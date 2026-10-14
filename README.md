# weavly-docs

Documentation site for the [Weavly](https://github.com/weavly-lang) dialogue scripting language and its tooling
(compiler and Godot addon).

Built with [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
Published to GitHub Pages at <https://weavly-lang.github.io/weavly-docs/> on every push to `main`.

## Local development

```bash
pip install -r requirements.txt "weavly==0.7.*"
mkdocs serve            # live-reloading preview at http://127.0.0.1:8000
mkdocs build --strict   # produce the static site in ./site
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and the checks.

## Structure

```
docs/
  index.md              # landing page
  getting-started.md
  language/             # the repo-agnostic language reference
  compiler/             # weavly CLI
  godot/                # Godot addon
  stylesheets/wvl.css   # the Godot editor's colors for Weavly code
hooks/wvl_names.py      # tells the highlighter what each name in the examples is
pygments-wvl/           # the Weavly highlighter, a port of the addon's
scripts/                # CI checks: examples compile, colors match the addon
mkdocs.yml              # site config + navigation
```
