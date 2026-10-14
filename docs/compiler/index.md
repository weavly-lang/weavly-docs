# Compiler (CLI)

The `weavly` command-line tool compiles `.wvl` files to JSON, which a runtime such as the [Godot addon](../godot/index.md) plays.

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
uv tool install "weavly==0.7.*"
```

With Python 3.11 or newer installed, `pipx install "weavly==0.7.*"` works too.

Weavly is in alpha, and the JSON output changes between releases without backward compatibility. Install the compiler version that matches your runtime: Godot addon 0.5 needs compiler 0.7.

Upgrade with `uv tool upgrade weavly`, and check the installed version with:

```bash
weavly --version
```

## Commands

### `weavly init`

Creates a new project with a starter file:

```bash
weavly init my-game
```

This creates `my-game/src/nodes.wvl`. Without a name, `weavly init` sets up the current folder. It refuses to overwrite: it stops if the folder `my-game`, or a `src` folder in the current folder, already exists.

### `weavly build`

Compiles every `.wvl` file of the project:

```bash
cd my-game
weavly build
```

Run it from the project root, the folder that holds `src`. `--pretty` writes indented JSON, which is easier to read when debugging:

```bash
weavly build --pretty
```

A successful build prints `Built 2 files into build/` and exits with code 0. A build with errors exits with code 1 and leaves the previous `build/` folder untouched, so a running game never loads half a build. See [Errors and warnings](diagnostics.md).

## Project layout

```text
my-game/
  src/              # your .wvl files, in any subfolders
    nodes.wvl
  build/            # written by weavly build, don't edit
    nodes.wvl.json
    env.json
```

The build writes one `.wvl.json` per source file, at the same path under `build/`, and one `env.json` with the declarations of the whole project. See [Build output](output.md).

In a Godot project, put the Weavly project in `res://dialogue`, so the addon finds `res://dialogue/build` without further setup.
