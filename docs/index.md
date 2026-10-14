# Weavly

Weavly is a scripting language for branching dialogue in games. You write conversations as plain text, the compiler checks them, and your game plays them.

```wvl
@env
character Guard
var has_pass: bool
@endenv

@node Gate
Guard: Halt! Who goes there?

@options
@option [has_pass] "Show the pass": @jump Town
@option "Turn back": @finish
@endoptions
@endnode

@node Town
The gate creaks open.
@endnode
```

- **Readable scripts.** Narration is plain text, dialogue is `Speaker: text`, and everything else starts with `@`.
- **Checked before you play.** The compiler catches typos, undeclared names and type errors, and points to the line.
- **Storylets built in.** Nodes can join pools with conditions, priorities and weights, so the game picks what fits.
- **No UI lock-in.** The Godot addon sends signals, and your game draws the dialogue however it likes, or uses a starter UI.

!!! info "Versions"
    These docs match compiler 0.7 and Godot addon 0.5. Weavly is in alpha: the language changes between releases without backward compatibility, so use the addon release that matches your compiler version.

## What's in these docs

- **[Getting Started](getting-started.md)**: install the compiler and build your first dialogue.
- **[Language Reference](language/index.md)**: everything you can write in a `.wvl` file.
- **[Compiler (CLI)](compiler/index.md)**: the `weavly` command-line tool.
- **[Godot Addon](godot/index.md)**: play compiled dialogue in Godot.

## The ecosystem

| Component | Repo |
| --- | --- |
| Compiler | [`weavly-lang/weavly-compiler`](https://github.com/weavly-lang/weavly-compiler) |
| Godot addon | [`weavly-lang/weavly-godot-addon`](https://github.com/weavly-lang/weavly-godot-addon) |
