"""Compiles every ```wvl block in docs/ with the installed weavly compiler and fails on errors.

A block without @node or @env is a fragment: it's wrapped in a node, and @option lines in an
@options block. Names a block uses without declaring come from DECLARATIONS and NODES, so a new
fragment that uses a new name needs it added there.
"""

import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
BLOCK = re.compile(r"^( *)```wvl\n(.*?)^\1```", re.S | re.M)
DECLARED = re.compile(r"^(?:@node|var|extern var|character|pool|slot|meta|func) +(\w+)", re.M)

DECLARATIONS = {
    "gold": "var gold: number = 20",
    "has_key": "var has_key: bool",
    "cursed": "var cursed: bool",
    "player_name": "var player_name: string",
    "greeting": "var greeting: string",
    "title": "var title: string",
    "visits": "var visits: number",
    "health": "var health: number(0, 100) = 100",
    "damage": "var damage: number",
    "mood": "var mood: string",
    "reputation": "var reputation: number",
    "scared": "var scared: bool",
    "met_guide": "var met_guide: bool",
    "guard_met": "var guard_met: bool",
    "has_sword": "var has_sword: bool",
    "has_shield": "var has_shield: bool",
    "allies": "var allies: number",
    "level": "var level: number",
    "lucky": "var lucky: bool",
    "danger": "var danger: number",
    "luck": "var luck: number",
    "base_price": "var base_price: number",
    "markup": "var markup: number",
    "has_tools": "var has_tools: bool",
    "next_step": "var next_step: node = Hall",
    "Guide": "character Guide",
    "Anna": "character Anna",
    "Ben": "character Ben",
    "camp_events": "pool camp_events",
    "forest_events": "pool forest_events",
    "weather_events": "pool weather_events",
    "cave_events": "pool cave_events",
    "camp_actions": "pool camp_actions",
    "night_actions": "pool night_actions",
    "cave_reward": "slot cave_reward",
    "cost": "meta cost: number = 0",
    "portrait": "func portrait(who: character, emotion: string)",
    "play_sound": "func play_sound(name: string, volume: number)",
    "shake_screen": "func shake_screen(strength: number)",
    "shake": "func shake(strength: number)",
    "save_game": "func save_game()",
    "trust": "func trust(from: character, to: character): number",
    "has_item": "func has_item(item: string): bool",
}
NODES = ["Hall", "Village", "Broke", "Chest", "Ship", "Alley", "Smithy", "Tavern", "Cave",
         "RentRoom", "HackTerminal", "Greeting"]


def project_files(block: str) -> dict[str, str]:
    defined = set(DECLARED.findall(block))
    if not re.search(r"^@(node|env)\b", block, re.M):
        if "@options" not in block:
            block = re.sub(r"^(@option .*\n)", r"@options\n\1@endoptions\n", block, flags=re.M)
        block = f"@node Snippet\n{block}@endnode\n"
    declarations = [line for name, line in DECLARATIONS.items() if name not in defined]
    nodes = "".join(
        f'@node {name}\n@meta\nlabel: "{name}"\n@endmeta\n{name}.\n@endnode\n'
        for name in NODES
        if name not in defined
    )
    return {"example.wvl": block, "prelude.wvl": "@env\n" + "\n".join(declarations) + "\n@endenv\n" + nodes}


def main() -> int:
    failed = checked = 0
    with tempfile.TemporaryDirectory() as work:
        for page in sorted(DOCS.rglob("*.md")):
            for match in BLOCK.finditer(page.read_text(encoding="utf-8")):
                block = textwrap.dedent(match.group(2))
                project = Path(work) / str(checked)
                (project / "src").mkdir(parents=True)
                for name, content in project_files(block).items():
                    (project / "src" / name).write_text(content, encoding="utf-8")
                result = subprocess.run(["weavly", "build"], cwd=project, capture_output=True, text=True)
                checked += 1
                if result.returncode != 0:
                    failed += 1
                    line = page.read_text(encoding="utf-8")[: match.start()].count("\n") + 1
                    errors = [l for l in (result.stdout + result.stderr).splitlines() if "error" in l]
                    print(f"{page.relative_to(DOCS).as_posix()}:{line}: example doesn't compile")
                    print(textwrap.indent("\n".join(errors), "    "))
    print(f"{checked - failed} of {checked} examples compile")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
