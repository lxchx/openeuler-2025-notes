#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_write_bytes(path: Path, data: bytes, *, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def extract_member(z: zipfile.ZipFile, member: str) -> bytes:
    try:
        with z.open(member, "r") as f:
            return f.read()
    except KeyError as e:
        raise FileNotFoundError(f"Zip member not found: {member}") from e


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract TalkDistill session bundles into GH Pages-friendly layout.")
    parser.add_argument(
        "--root",
        default=".",
        help="Site root directory (default: current directory)",
    )
    parser.add_argument(
        "--manifest",
        default="data/manifest.json",
        help="Manifest path relative to --root (default: data/manifest.json)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing extracted files",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest_path = (root / args.manifest).resolve()
    if not manifest_path.exists():
        print(f"[ERR] manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    manifest = read_json(manifest_path)
    sessions = manifest.get("sessions", [])
    if not isinstance(sessions, list) or not sessions:
        print("[ERR] manifest.sessions is empty", file=sys.stderr)
        return 2

    out_parts_dir = root / "packages" / "parts"
    out_sessions_dir = root / "data" / "sessions"
    out_parts_dir.mkdir(parents=True, exist_ok=True)
    out_sessions_dir.mkdir(parents=True, exist_ok=True)

    for s in sessions:
        sid = str(s.get("id", "")).strip()
        bundle_rel = str(s.get("bundle_zip", "")).strip()
        if not sid or not bundle_rel:
            print(f"[WARN] skip invalid session entry: {s!r}", file=sys.stderr)
            continue

        bundle_path = (root / bundle_rel).resolve()
        if not bundle_path.exists():
            print(f"[WARN] bundle not found, skip: {bundle_path}", file=sys.stderr)
            continue

        print(f"[INFO] session={sid} bundle={bundle_path}")
        with zipfile.ZipFile(bundle_path, "r") as z:
            overview_bytes = extract_member(z, "session_overview.json")
            index_bytes = extract_member(z, "session_index.json")

            sess_dir = out_sessions_dir / sid
            safe_write_bytes(sess_dir / "session_overview.json", overview_bytes, force=args.force)
            safe_write_bytes(sess_dir / "session_index.json", index_bytes, force=args.force)

            try:
                index = json.loads(index_bytes.decode("utf-8"))
            except Exception as e:
                print(f"[WARN] failed to parse session_index.json for {sid}: {e}", file=sys.stderr)
                continue

            parts = index.get("parts", [])
            if not isinstance(parts, list) or not parts:
                print(f"[WARN] no parts found in session_index.json for {sid}", file=sys.stderr)
                continue

            for p in parts:
                archive = str((p or {}).get("archive") or (p or {}).get("name") or "").strip()
                if not archive:
                    continue
                out_path = out_parts_dir / archive
                if out_path.exists() and not args.force:
                    raise FileExistsError(f"Refusing to overwrite existing part archive: {out_path}")
                data = extract_member(z, archive)
                safe_write_bytes(out_path, data, force=args.force)
                print(f"  - part: {archive} -> {out_path.relative_to(root)}")

    print("[DONE] extraction complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

