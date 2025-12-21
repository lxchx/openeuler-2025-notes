# openEuler-2025-notes（GitHub Pages）

这个目录是一份可直接部署到 GitHub Pages 的静态站点：

- `index.html`：会场入口（Day1/Day2 主会场 + 分会场）
- `show.html`：TalkDistill Viewer（支持 session 总览、part 视图、section 直链定位）

## 直链导航（URL）

站点支持用 URL 直接定位到某个会场/part/section：

- 会场总览：`show.html?session=ai_session`
- 指定 part：`show.html?session=ai_session&part=0`
- 指定 section：`show.html?session=ai_session&part=0&sec=sec_3`

说明：

- `session`：会场/会话 ID（见 `data/manifest.json`）
- `part`：该会话里的 part 索引（数字）
- `sec`：该 part 里的 section id（例如 `sec_3`）

## 数据组织

- `data/manifest.json`：站点清单（会场列表、索引/总览 JSON 路径、part 包路径前缀、视频路径前缀）
- `data/sessions/<session>/session_index.json`、`data/sessions/<session>/session_overview.json`：从 session bundle 抽取的总览/索引
- `packages/parts-lite/*.tkd.zip`：各 part 的轻量包（**不含视频**，供 show.html 优先按需加载，避免 zip 内视频阻塞解析）
- `packages/videos/<session>/part_XX_low.mp4`：独立视频文件（浏览器可 Range/流式加载，不阻塞其它数据渲染）
- `packages/parts/*.tkd.zip`：从 session bundle 抽取的各 part 原始包（保留作为来源/兜底）

## 重新抽取（从 session bundle 解出 parts/与 sessions/）

在 `openeuler-2025-notes/` 目录下执行：

- `python3 tools/extract_packages.py`

默认拒绝覆盖已存在的文件；如需强制覆盖可加 `--force`。

说明：`tools/extract_packages.py` 需要 session bundle（例如 `ai_session.tkd.zip`）作为输入；为了减小仓库体积，这些 bundle 默认不放在 `packages/` 下。

## 拆分视频（把 part 包拆到“视频级别”）

在 `openeuler-2025-notes/` 目录下执行：

- `python3 tools/split_parts_for_pages.py --root .`

它会从 `packages/parts/*.tkd.zip` 生成：

- `packages/parts-lite/*.tkd.zip`（去掉 `.mp4/.mov/...`）
- `packages/videos/<session>/part_XX_low.mp4`（导出 `part_low.mp4`，若找不到则兜底导出任意 `.mp4`）

注意：GitHub 仓库对大文件有体积限制，独立 mp4 仍可能需要 Git LFS / Release / 外部对象存储。

## 部署到 GitHub Pages

常见做法：

已提供 GitHub Actions 自动部署：`.github/workflows/pages.yml` 会把 `openeuler-2025-notes/` 发布到 GitHub Pages。

注意：workflow 默认不会发布 `packages/parts/`（仅保留 `parts-lite/` + `videos/`），以避免站点体积膨胀；如果你确实需要发布原始 part 包，再调整 workflow 的 rsync exclude。

## 本地预览

建议用带 Range 支持的预览脚本（否则视频无法按需分段加载，点击跳转可能会“卡在开头”）：

- `python3 tools/serve_preview.py --root . --port 8899`
