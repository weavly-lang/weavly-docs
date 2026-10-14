# Godot Addon

The Godot addon plays compiled Weavly dialogue in your game. It also adds a `.wvl` editor to Godot that compiles your scripts with one click.

## Requirements

- Godot 4.5 or newer.
- For the editor tooling: the Weavly compiler 0.7, see [Compiler (CLI)](../compiler/index.md#installation). Games you export don't need the compiler.

## Installation

1. Download `weavly-<version>.zip` from the [releases](https://github.com/weavly-lang/weavly-godot-addon/releases) and extract it into your project, so the addon lands in `addons/weavly`.
2. Enable **Weavly** under *Project → Project Settings → Plugins*.
3. Install the compiler, then restart Godot so it finds it:

    ```bash
    uv tool install "weavly==0.7.*"
    ```

The addon finds the compiler as `weavly` on your `PATH`. If it's installed somewhere else, set *Editor Settings → Weavly → Executable Path*, see [Editor](editor.md#settings).

## Where the dialogue lives

The engine loads compiled dialogue from `res://dialogue/build` by default. Keep your Weavly project in `res://dialogue`:

```text
res://
  addons/weavly/
  dialogue/
    src/      # your .wvl files
    build/    # compiled JSON, loaded by the engine
```

To use another folder, set the engine's `dialogue_path`, see [Running dialogue](engine.md#settings).

## Exporting

The compiled dialogue is JSON, which Godot doesn't export by default. In each export preset, add `*.json` to *Resources → Filters to export non-resource files/folders*.

## Next steps

Follow the [Quick start](quickstart.md) to play your first dialogue.
