# openeuler-2025-notes Overview

Static GitHub Pages site for TalkDistill outputs.

## Structure
- `index.html`: entry page to pick session and part.
- `show.html`: viewer page with video, transcript, slides, and graph.
- `data/manifest.json`: site registry.
- `packages/parts-web/<session>/part_XX/`: web-ready assets for on-demand load.
- `packages/videos/<session>/`: mp4 video files (separate from text/json).

## Viewer URL
- `show.html?session=<name>&part=<n>&sec=sec_XXX` opens a section.
- `hit` supports plain text or regex (`/pattern/flags`) within the section.
- After load, the viewer re-aligns scroll to avoid layout shifts.
- `hit` highlight works across markdown nodes (bold/list/line breaks).

## Docs
- `docs/analysis-draft.md` is the source markdown.
- CI builds `analysis-draft.html` from `templates/md_viewer_template.html` via `tools/build_docs.py`.
- The HTML page provides sticky TOC, heading/list collapse, and reading progress.
- Links to `show.html?session=...&part=...&sec=...` show a hover preview with highlighted `hit`, full section content, and async slide thumbs.

## Asset prep
- `tools/split_parts_for_pages.py --viewer-only`: create slim `.tkd.zip` for viewer.
- `tools/export_parts_web.py`: unpack to `packages/parts-web` for progressive load.
- `tools/extract_packages.py`: extract `data/sessions/*` from `.tkd.zip` (no overwrite).

## Deployment
- GitHub Pages serves `openeuler-2025-notes/` as a static site.
