# Build output

`weavly build` writes the compiled project into `build/`:

| File | Holds |
|---|---|
| `build/<path>.wvl.json` | the nodes of `src/<path>.wvl`, one file per source file |
| `build/env.json` | every declaration of the project: variables, characters, pools, slots, meta keys and functions |

Runtimes load the whole folder. The Godot addon reads it from `res://dialogue/build` by default, see [Godot Addon](../godot/index.md).

Never edit these files by hand: the next build replaces them.

!!! warning "The format isn't stable"
    The JSON format is internal to the compiler and the runtimes. It changes between releases without backward compatibility, so always use a runtime that matches your compiler version: these docs match compiler 0.7.

To look at the output while debugging, build with `--pretty` for indented JSON.
