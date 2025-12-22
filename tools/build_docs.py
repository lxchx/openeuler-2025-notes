#!/usr/bin/env python3
import argparse
import html
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build static HTML docs from markdown template.")
    parser.add_argument("--input", required=True, help="Path to markdown source")
    parser.add_argument("--template", required=True, help="HTML template path")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--title", default="Analysis Draft", help="HTML title")
    args = parser.parse_args()

    md_path = Path(args.input)
    tpl_path = Path(args.template)
    out_path = Path(args.output)

    md_text = md_path.read_text(encoding="utf-8")
    tpl_text = tpl_path.read_text(encoding="utf-8")

    escaped = html.escape(md_text)
    escaped = escaped.replace("</script>", "<\\/script>")

    rendered = tpl_text.replace("{{MD_CONTENT}}", escaped).replace("{{TITLE}}", args.title)
    out_path.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
