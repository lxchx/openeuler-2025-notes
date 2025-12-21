#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import os
import re
import socket
import sys
from contextlib import closing
from pathlib import Path


def can_bind(host: str, port: int) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def pick_port(host: str, port: int, auto: bool) -> int:
    if port == 0:
        return 0
    if can_bind(host, port):
        return port
    if not auto:
        raise OSError(f"Port in use: {port}")
    for p in range(port + 1, port + 21):
        if can_bind(host, p):
            return p
    raise OSError(f"No free port found in range [{port}, {port+20}]")


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve openeuler-2025-notes for local preview.")
    parser.add_argument("--root", default="openeuler-2025-notes", help="Site root directory")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8899, help="Bind port (default: 8899, use 0 for random)")
    parser.add_argument(
        "--auto-port",
        action="store_true",
        default=True,
        help="If port is busy, try next ports (default: true)",
    )
    parser.add_argument(
        "--no-auto-port",
        action="store_false",
        dest="auto_port",
        help="Disable auto port fallback",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[ERR] root not found: {root}", file=sys.stderr)
        return 2

    os.chdir(root)

    port = pick_port(args.host, args.port, args.auto_port)
    if port == 0:
        port = 0

    from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

    class RangeRequestHandler(SimpleHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def __init__(self, *args, **kwargs):
            self._byte_range: tuple[int, int, int] | None = None
            super().__init__(*args, **kwargs)

        def end_headers(self) -> None:
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "no-cache")
            super().end_headers()

        def send_head(self):
            self._byte_range = None

            path = self.translate_path(self.path)
            if os.path.isdir(path):
                parts = self.path.split("?", 1)
                self.path = parts[0]
                return super().send_head()

            ctype = self.guess_type(path)
            try:
                f = open(path, "rb")
            except OSError:
                self.send_error(404, "File not found")
                return None

            try:
                fs = os.fstat(f.fileno())
                size = int(fs.st_size)

                range_header = self.headers.get("Range")
                if range_header:
                    m = re.match(r"^bytes=(\d*)-(\d*)$", range_header.strip())
                    if m:
                        start_s, end_s = m.group(1), m.group(2)
                        if start_s == "" and end_s == "":
                            start, end = 0, size - 1
                        elif start_s == "":
                            suffix = int(end_s)
                            suffix = max(0, min(suffix, size))
                            start, end = size - suffix, size - 1
                        else:
                            start = int(start_s)
                            end = int(end_s) if end_s != "" else size - 1

                        if start < 0 or start >= size:
                            f.close()
                            self.send_response(416)
                            self.send_header("Content-Range", f"bytes */{size}")
                            self.send_header("Content-Length", "0")
                            self.end_headers()
                            return None

                        end = max(start, min(end, size - 1))
                        self._byte_range = (start, end, size)
                        self.send_response(206)
                        self.send_header("Content-type", ctype)
                        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                        self.send_header("Content-Length", str(end - start + 1))
                        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                        self.end_headers()
                        return f

                self.send_response(200)
                self.send_header("Content-type", ctype)
                self.send_header("Content-Length", str(size))
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.end_headers()
                return f
            except Exception:
                try:
                    f.close()
                except Exception:
                    pass
                raise

        def copyfile(self, source, outputfile):
            if self._byte_range:
                start, end, _ = self._byte_range
                source.seek(start)
                remaining = end - start + 1
                bufsize = 64 * 1024
                while remaining > 0:
                    chunk = source.read(min(bufsize, remaining))
                    if not chunk:
                        break
                    outputfile.write(chunk)
                    remaining -= len(chunk)
                return
            return super().copyfile(source, outputfile)

    httpd = ThreadingHTTPServer((args.host, port), RangeRequestHandler)
    actual_port = httpd.server_address[1]

    print(f"[OK] Serving: http://{args.host}:{actual_port}/")
    print(f"[OK] Entry:   http://{args.host}:{actual_port}/index.html")
    print(f"[OK] Example: http://{args.host}:{actual_port}/show.html?session=ai_session&part=0&sec=sec_3")
    print("[OK] Press Ctrl+C to stop.")
    sys.stdout.flush()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[OK] Stopped.")
        return 0
    finally:
        try:
            httpd.server_close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
