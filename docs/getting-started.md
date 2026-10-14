# Getting Started

This page takes you from nothing to a compiled dialogue. To play it in a game, continue with the [Godot quick start](godot/quickstart.md).

## Install the compiler

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then the Weavly compiler:

```bash
uv tool install "weavly==0.7.*"
```

Check that it works:

```bash
weavly --version
```

## Create a project

```bash
weavly init my-game
cd my-game
```

This creates `src/nodes.wvl`:

```wvl
@env
character Guide
var name: string = "World"
@endenv

@node FirstNode
Guide: Hello {name}!
@endnode
```

- `@env` declares what the script uses: a character called `Guide` and a text variable `name`.
- `@node FirstNode` is a piece of dialogue the game can start.
- `Guide: Hello {name}!` is a line spoken by the guide, with the variable's value put into the text.

## Write some dialogue

Replace the file's contents with a short conversation with a choice:

```wvl
@env
character Guide
var name: string = "World"
var asked: bool
@endenv

@node FirstNode
Guide: Hello {name}!
Guide: What brings you here?

@options
@option "Just looking around.": Guide: Take your time.
@option "I'm lost."
    @set asked = true
    Guide: Follow the river and you'll find the village.
@endoptions

@if asked: Guide: Safe travels.
@endnode
```

## Build it

```bash
weavly build
```

The compiler checks the whole project and writes the result to `build/`. If something is wrong, it tells you where. Forgetting `@endoptions`, for example, gives:

```text
src/nodes.wvl:16:1: error: unexpected '@endnode'
  16 | @endnode
     | ^
  hint: the @options block opened at line 11 must be closed with @endoptions first
```

## Next steps

- Play the dialogue in Godot with the [Godot quick start](godot/quickstart.md).
- Learn the language in the [Language Reference](language/index.md).
- See every compiler command in [Compiler (CLI)](compiler/index.md).
