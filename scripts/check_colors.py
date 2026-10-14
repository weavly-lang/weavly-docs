"""Fails when docs/stylesheets/wvl.css and the addon's WvlSyntaxHighlighter colors differ.

Usage: python scripts/check_colors.py <path to wvl_syntax_highlighter.gd>
"""

import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "docs" / "stylesheets" / "wvl.css"


def main() -> int:
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    godot = {
        name.lower(): "#" + "".join(f"{int(float(c) * 255 + 0.5):02x}" for c in rgb.split(",")[:3])
        for name, rgb in re.findall(r"^const (\w+)_COLOR = Color\(([^)]*)\)", source, re.M)
    }
    css = dict(re.findall(r"--wvl-([\w-]+): (#[0-9a-f]{6});", CSS.read_text(encoding="utf-8")))
    css.pop("background")
    mismatches = [
        f"{name}: addon {godot.get(name)}, docs {css.get(name)}"
        for name in sorted(godot.keys() | css.keys())
        if godot.get(name) != css.get(name)
    ]
    for mismatch in mismatches:
        print(mismatch)
    if not mismatches:
        print(f"{len(godot)} colors match")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
