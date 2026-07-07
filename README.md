# weavly-docs

Documentation site for the [Weavly](https://github.com/weavly-lang) dialog scripting language and its tooling
(compiler, Godot addon, VS Code extension).

Built with [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
Published to GitHub Pages at <https://weavly-lang.github.io/weavly-docs/> on every push to `main`.

## Local development

```bash
pip install -r requirements.txt
mkdocs serve            # live-reloading preview at http://127.0.0.1:8000
mkdocs build --strict   # produce the static site in ./site
```

## Structure

```
docs/
  index.md              # landing page
  getting-started.md
  language/             # the repo-agnostic language reference
  compiler/             # weavly CLI
  godot/                # Godot addon
  vscode/               # VS Code extension
mkdocs.yml              # site config + navigation
```
