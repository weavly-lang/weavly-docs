"""Gives the Weavly lexer the names declared or used across the site, the current page's first."""

import re
from pathlib import Path

import weavly_pygments

_BLOCK = re.compile(r"^( *)```wvl\n(.*?)^\1```", re.S | re.M)
_site_names: dict[str, str] = {}


def _sources(markdown: str) -> list[str]:
    return [match.group(2) for match in _BLOCK.finditer(markdown)]


def on_files(files, config):
    sources = []
    for path in sorted(Path(config["docs_dir"]).rglob("*.md")):
        sources += _sources(path.read_text(encoding="utf-8"))
    _site_names.clear()
    _site_names.update(weavly_pygments.collect_names(sources))
    return files


def on_page_markdown(markdown, page, config, files):
    weavly_pygments.NAMES = {**_site_names, **weavly_pygments.collect_names(_sources(markdown))}
    return markdown
