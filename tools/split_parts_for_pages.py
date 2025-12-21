#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PartId:
    session: str
    index: int

    @property
    def index2(self) -> str:
        return f"{self.index:02d}"


PART_NAME_RE = re.compile(r"^(?P<session>.+?)_part_(?P<idx>\d+)\.tkd\.zip$", re.IGNORECASE)


def parse_part_id(filename: str) -> PartId | None:
    m = PART_NAME_RE.match(filename)
    if not m:
        return None
    session = str(m.group("session")).strip()
    idx = int(m.group("idx"))
    if not session:
        return None
    return PartId(session=session, index=idx)


def should_drop_from_lite(path: str) -> bool:
    lower = path.lower()
    return lower.endswith(".mp4") or lower.endswith(".mov") or lower.endswith(".mkv") or lower.endswith(".webm")


KEEP_FOR_VIEWER: list[re.Pattern[str]] = [
    re.compile(r"(^|/)part_subtitles(_aligned)?\.srt$", re.IGNORECASE),
    re.compile(r"(^|/)chunk_subtitles(_aligned)?\.srt$", re.IGNORECASE),
    re.compile(r"(^|/)section_manifest(_aligned)?\.json$", re.IGNORECASE),
    re.compile(r"(^|/)section_graph\.json$", re.IGNORECASE),
    re.compile(r"(^|/)materials\.json$", re.IGNORECASE),
    re.compile(r"(^|/)material_manifest\.json$", re.IGNORECASE),
    re.compile(r"(^|/)section_.+_narrative\.json$", re.IGNORECASE),
    re.compile(r"(^|/)section_.+_refined\.md$", re.IGNORECASE),
    re.compile(
        r"/\d+_capture_frame/slide_\d+/artifacts/slide_\d+\.(?:png|jpg|jpeg|webp)$",
        re.IGNORECASE,
    ),
]


def should_keep_for_viewer(path: str) -> bool:
    return any(p.search(path) for p in KEEP_FOR_VIEWER)


def pick_part_low_video(members: list[str]) -> str | None:
    lowers = [(m, m.lower()) for m in members]
    candidates = [m for (m, l) in lowers if l.endswith("part_low.mp4")]
    if candidates:
        candidates.sort(key=lambda p: (0 if p.startswith("final/") or "/final/" in p else 1, len(p)))
        return candidates[0]
    any_mp4 = [m for (m, l) in lowers if l.endswith(".mp4")]
    if any_mp4:
        any_mp4.sort(key=lambda p: len(p))
        return any_mp4[0]
    return None


def safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def refuse_overwrite(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Split TalkDistill part archives for GH Pages: create lite zip (no video) + export mp4. "
            "Optionally build a viewer-only lite zip that keeps only files required by show.html."
        )
    )
    parser.add_argument("--root", default=".", help="Site root (default: current dir)")
    parser.add_argument("--parts-dir", default="packages/parts", help="Full part zips dir (default: packages/parts)")
    parser.add_argument(
        "--out-lite-dir",
        default="packages/parts-lite",
        help="Output dir for lite part zips (default: packages/parts-lite)",
    )
    parser.add_argument(
        "--out-video-dir",
        default="packages/videos",
        help="Output base dir for videos (default: packages/videos)",
    )
    parser.add_argument(
        "--no-video",
        action="store_true",
        help="Do not export mp4 (only build lite zips)",
    )
    parser.add_argument(
        "--viewer-only",
        action="store_true",
        help="Keep only minimal files for show.html (reduces zip size further)",
    )
    parser.add_argument(
        "--only",
        default="",
        help="Optional regex filter on part zip filename (case-insensitive)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    parts_dir = (root / args.parts_dir).resolve()
    out_lite_dir = (root / args.out_lite_dir).resolve()
    out_video_dir = (root / args.out_video_dir).resolve()

    if not parts_dir.exists():
        print(f"[ERR] parts dir not found: {parts_dir}", file=sys.stderr)
        return 2

    safe_mkdir(out_lite_dir)
    safe_mkdir(out_video_dir)

    zips = sorted([p for p in parts_dir.iterdir() if p.is_file() and p.name.lower().endswith(".tkd.zip")])
    if not zips:
        print(f"[ERR] no part zips found under: {parts_dir}", file=sys.stderr)
        return 2

    only_re: re.Pattern[str] | None = None
    if args.only:
        only_re = re.compile(str(args.only), re.IGNORECASE)
        zips = [p for p in zips if only_re.search(p.name)]
        if not zips:
            print(f"[ERR] no part zips matched --only={args.only!r}", file=sys.stderr)
            return 2

    for src in zips:
        pid = parse_part_id(src.name)
        if not pid:
            print(f"[WARN] skip unmatched filename: {src.name}", file=sys.stderr)
            continue

        lite_path = out_lite_dir / src.name
        refuse_overwrite(lite_path, args.force)

        video_rel = Path(pid.session) / f"part_{pid.index2}_low.mp4"
        video_path = out_video_dir / video_rel
        if not args.no_video:
            refuse_overwrite(video_path, args.force)
            safe_mkdir(video_path.parent)

        if args.no_video:
            print(f"[INFO] {src.name} -> {lite_path.relative_to(root)}")
        else:
            print(f"[INFO] {src.name} -> {lite_path.relative_to(root)} + {video_path.relative_to(root)}")

        with zipfile.ZipFile(src, "r") as zin:
            members = [zi.filename for zi in zin.infolist() if not zi.is_dir()]
            if not args.no_video:
                video_member = pick_part_low_video(members)
                if not video_member:
                    print(f"[WARN] no mp4 found in {src.name}", file=sys.stderr)
                else:
                    with zin.open(video_member, "r") as fsrc, open(video_path, "wb") as fdst:
                        fdst.write(fsrc.read())

            with zipfile.ZipFile(lite_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                for zi in zin.infolist():
                    if zi.is_dir():
                        continue
                    if should_drop_from_lite(zi.filename):
                        continue
                    if args.viewer_only and not should_keep_for_viewer(zi.filename):
                        continue
                    data = zin.read(zi.filename)
                    zout.writestr(zi, data)

    print("[DONE] split complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
