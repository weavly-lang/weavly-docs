# Contributing

## Workflow

Every change starts from a GitHub issue and lands on `main` as one squashed commit.

1. `gh issue develop <number> --checkout` creates and links the `<number>-<slug>` branch.
2. Commit freely. Commits are squashed on merge. Rebase on `origin/main` when it moves ahead.
3. `gh pr create --title "<sentence, usually the issue title>" --body "Closes #<number>"`. The title becomes the commit message on `main`.
4. Squash and merge once CI passes. Merging to `main` publishes the site.

Changes to the language or the Godot addon's behaviour start as an issue here, filed from the compiler or addon change that needs them.

## Local preview

```bash
pip install -r requirements.txt "weavly==0.7.*"
mkdocs serve
```

The site reloads at <http://127.0.0.1:8000> as you edit. `requirements.txt` installs the Weavly code highlighter from `pygments-wvl/` in editable mode.

## Checks

CI runs these before it publishes, and fails on any of them:

```bash
python scripts/check_examples.py
python scripts/check_colors.py ../weavly-godot-addon/addons/weavly/editor/wvl_syntax_highlighter.gd
mkdocs build --strict
```

- `check_examples.py` compiles every ```` ```wvl ```` block with the installed compiler. A block without `@node` or `@env` is a fragment and gets wrapped in a node. Names a fragment uses without declaring come from `DECLARATIONS` and `NODES` in the script, so add new ones there.
- `check_colors.py` compares `docs/stylesheets/wvl.css` with the color constants of the addon's `.wvl` editor. Change both together.
- `mkdocs build --strict` fails on broken links and anchors.

CI runs on every PR and every push to `main`, with the compiler pinned. A weekly run, `upstream-latest.yml`, checks the examples against the newest compiler release and the colors against the addon's `main`. When it fails, the docs need an update for what changed upstream.

## Writing

- Tag Weavly code ```` ```wvl ```` and GDScript ```` ```gdscript ````. Indent GDScript with tabs, like Godot's script editor, so it pastes cleanly.
- Examples follow the naming convention: PascalCase nodes and characters, snake_case everything else. The highlighter relies on it for names an example doesn't declare.
- The language pages describe the language, not a runtime. Godot specifics go in the Godot pages, linked from the language pages where they matter.
- Describe what the compiler and the addon do now, checked against their code, not the notes they started from.

## Releases

The docs match one compiler and addon version, named on the landing page. When a new version changes the language or the addon:

1. Update the pages it changes.
2. Update the versions on the landing page, in `docs/compiler/index.md`, `docs/getting-started.md` and `docs/godot/index.md`.
3. Update the compiler version in `.github/workflows/deploy.yml` and in the local preview above.
