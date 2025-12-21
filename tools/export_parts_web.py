#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
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


def safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def refuse_overwrite(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite: {path}")


def in_final(name: str) -> bool:
    return "/final/" in name or name.startswith("final/")


def in_chunk(name: str) -> bool:
    return "/chunk_" in name or name.startswith("chunk_")


def chunk_key_from_path(p: str) -> str | None:
    m = re.search(r"(^|/)(chunk_[^/]+)/", str(p))
    return str(m.group(2)) if m else None


def filename_no_ext(p: str) -> str:
    name = str(p).split("/")[-1] if p else ""
    return re.sub(r"\.[^.]+$", "", name)


def pick_best(cands: list[dict]) -> str | None:
    if not cands:
        return None
    cands.sort(key=lambda x: int(x.get("rank", 999999)))
    return str(cands[0]["name"])


def write_json(path: Path, data: object) -> None:
    safe_mkdir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export TalkDistill part-lite zips into a web-friendly directory format so show.html can load "
            "small JSON/MD/SRT first (no need to download an entire zip before rendering)."
        )
    )
    parser.add_argument("--root", default=".", help="Site root (default: current dir)")
    parser.add_argument(
        "--in-lite-dir",
        default="packages/parts-lite",
        help="Input dir of lite part zips (default: packages/parts-lite)",
    )
    parser.add_argument(
        "--out-web-dir",
        default="packages/parts-web",
        help="Output base dir for web parts (default: packages/parts-web)",
    )
    parser.add_argument(
        "--only",
        default="",
        help="Optional regex filter on part zip filename (case-insensitive)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    in_lite_dir = (root / args.in_lite_dir).resolve()
    out_web_dir = (root / args.out_web_dir).resolve()

    if not in_lite_dir.exists():
        print(f"[ERR] input dir not found: {in_lite_dir}", file=sys.stderr)
        return 2

    safe_mkdir(out_web_dir)

    zips = sorted([p for p in in_lite_dir.iterdir() if p.is_file() and p.name.lower().endswith(".tkd.zip")])
    if not zips:
        print(f"[ERR] no lite part zips found under: {in_lite_dir}", file=sys.stderr)
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

        out_part_dir = out_web_dir / pid.session / f"part_{pid.index2}"
        out_manifest = out_part_dir / "manifest.json"
        refuse_overwrite(out_manifest, args.force)

        print(f"[INFO] {src.name} -> {out_manifest.relative_to(root)}")

        with zipfile.ZipFile(src, "r") as zin:
            members = [zi.filename for zi in zin.infolist() if not zi.is_dir()]

            srt_candidates: list[dict] = []
            nar_files: list[dict] = []
            ref_files: list[dict] = []
            capture_by_id: dict[str, str] = {}
            sec_manifest_aligned: str | None = None
            sec_manifest_plan: str | None = None
            sec_manifest_any: str | None = None
            graph_final: str | None = None
            graph_any: str | None = None
            materials_final: str | None = None
            materials_any: str | None = None
            material_manifest_any: str | None = None

            for name in members:
                lower = name.lower()
                is_final = in_final(name)
                is_chunk = in_chunk(name)

                if lower.endswith("part_subtitles_aligned.srt"):
                    srt_candidates.append({"rank": 0 if is_final else 10, "name": name})
                elif lower.endswith("part_subtitles.srt"):
                    srt_candidates.append({"rank": 1 if is_final else 11, "name": name})
                elif lower.endswith("chunk_subtitles_aligned.srt"):
                    srt_candidates.append({"rank": 2 if is_chunk else 12, "name": name})
                elif lower.endswith("chunk_subtitles.srt"):
                    srt_candidates.append({"rank": 3 if is_chunk else 13, "name": name})

                if is_final and lower.endswith("section_manifest_aligned.json") and not sec_manifest_aligned:
                    sec_manifest_aligned = name
                if is_final and lower.endswith("section_manifest.json") and not sec_manifest_plan:
                    sec_manifest_plan = name
                if lower.endswith("section_manifest.json") and not sec_manifest_any:
                    sec_manifest_any = name

                if is_final and re.search(r"_merge_slides/artifacts/materials\.json$", name, re.I) and not materials_final:
                    materials_final = name
                if re.search(r"materials\.json$", name, re.I) and not materials_any:
                    materials_any = name
                if lower.endswith("material_manifest.json") and not material_manifest_any:
                    material_manifest_any = name

                if is_final and lower.endswith("section_graph.json") and not graph_final:
                    graph_final = name
                if lower.endswith("section_graph.json") and not graph_any:
                    graph_any = name

                m_nar = re.search(r"section_(.+)_narrative\.json$", name, re.I)
                if m_nar:
                    nar_files.append({"sid": m_nar.group(1), "path": name, "final": 1 if is_final else 0})
                m_ref = re.search(r"section_(.+)_refined\.md$", name, re.I)
                if m_ref:
                    ref_files.append({"sid": m_ref.group(1), "path": name, "final": 1 if is_final else 0})

                if re.search(r"/\d+_capture_frame/", name) and re.search(r"slide_\d+\.png$", name, re.I):
                    ck = chunk_key_from_path(name)
                    slide_id = filename_no_ext(name)
                    if ck and slide_id:
                        capture_by_id[f"{ck}/{slide_id}"] = name

            srt_path = pick_best(srt_candidates)
            sec_manifest_path = sec_manifest_aligned or sec_manifest_plan or sec_manifest_any
            graph_path = graph_final or graph_any
            materials_path = materials_final or materials_any

            if not srt_path:
                raise RuntimeError(f"{src.name}: 未找到字幕产物（part_subtitles_aligned.srt 或 chunk_subtitles_aligned.srt）")
            if not sec_manifest_path:
                raise RuntimeError(f"{src.name}: 未找到 section_manifest")

            # Parse section manifest to know which captures are actually referenced.
            sec_json = json.loads(zin.read(sec_manifest_path))
            sections = sec_json.get("sections", sec_json if isinstance(sec_json, list) else [])
            referenced_material_ids: set[str] = set()
            for s in sections or []:
                for mid in (s.get("material_ids") or []):
                    referenced_material_ids.add(str(mid))

            # Materials meta (optional).
            materials_by_id: dict[str, dict] = {}
            if materials_path and materials_path in members:
                try:
                    m_json = json.loads(zin.read(materials_path))
                    items = m_json.get("materials") if isinstance(m_json, dict) else m_json
                    if isinstance(items, list):
                        for m in items:
                            if m and isinstance(m, dict) and m.get("id"):
                                materials_by_id[str(m["id"])] = m
                except Exception:
                    pass
            elif material_manifest_any and material_manifest_any in members:
                try:
                    m_json = json.loads(zin.read(material_manifest_any))
                    items = m_json.get("materials") if isinstance(m_json, dict) else m_json
                    if isinstance(items, list):
                        for m in items:
                            if m and isinstance(m, dict) and m.get("id"):
                                materials_by_id[str(m["id"])] = m
                except Exception:
                    pass

            # Keep best version for each section doc.
            nar_files.sort(key=lambda x: (-int(x.get("final", 0)), str(x.get("path", ""))))
            ref_files.sort(key=lambda x: (-int(x.get("final", 0)), str(x.get("path", ""))))
            refined_paths_by_sid: dict[str, str] = {}
            narrative_paths_by_sid: dict[str, str] = {}
            for f in nar_files:
                sid = str(f["sid"])
                if sid not in narrative_paths_by_sid:
                    narrative_paths_by_sid[sid] = str(f["path"])
            for f in ref_files:
                sid = str(f["sid"])
                if sid not in refined_paths_by_sid:
                    refined_paths_by_sid[sid] = str(f["path"])

            # Only export captures that are referenced by sections/materials.
            captures_export: dict[str, str] = {}
            for mid in sorted(referenced_material_ids):
                p = capture_by_id.get(mid)
                if p:
                    captures_export[mid] = p
                else:
                    # Some sections may have no slide; skip quietly.
                    pass

            files = {
                "srt": srt_path,
                "section_manifest": sec_manifest_path,
                "section_manifest_plan": sec_manifest_plan,
                "materials": materials_path,
                "material_manifest": material_manifest_any,
                "graph": graph_path,
                "refined": refined_paths_by_sid,
                "narratives": narrative_paths_by_sid,
                "captures": captures_export,
            }

            # Extract files to disk (keep original relative paths).
            out_files: set[str] = set()
            for k in ("srt", "section_manifest", "section_manifest_plan", "materials", "material_manifest", "graph"):
                p = files.get(k)
                if p and isinstance(p, str) and p in members:
                    out_files.add(p)
            out_files.update(v for v in refined_paths_by_sid.values() if v in members)
            out_files.update(v for v in narrative_paths_by_sid.values() if v in members)
            out_files.update(v for v in captures_export.values() if v in members)

            for rel in sorted(out_files):
                out_path = out_part_dir / rel
                refuse_overwrite(out_path, args.force)
                safe_mkdir(out_path.parent)
                with zin.open(rel, "r") as fsrc, open(out_path, "wb") as fdst:
                    fdst.write(fsrc.read())

            manifest = {
                "format": "talkdistill_part_web_v1",
                "session": pid.session,
                "index": pid.index,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source_zip": str(Path(args.in_lite_dir) / src.name),
                "files": files,
                "_meta": {
                    "sections": len(sections) if isinstance(sections, list) else 0,
                    "refined_sections": len(refined_paths_by_sid),
                    "captures": len(captures_export),
                    "materials": len(materials_by_id),
                },
            }
            write_json(out_manifest, manifest)

    print("[DONE] export complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

