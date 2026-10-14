# Language Reference

Weavly is a language for writing branching dialogue. You write `.wvl` files, the [compiler](../compiler/index.md) turns them into JSON, and a runtime such as the [Godot addon](../godot/index.md) plays that JSON in your game.

```
@env
character Guide
var met_guide: bool
@endenv

@node Welcome
@if met_guide
    Guide: Back again?
@else
    Guide: Hello, traveller.
    @set met_guide = true
@endif

@options
@option "Ask about the village": @detour Village
@option "Leave": @finish
@endoptions
@endnode

@node Village
Guide: It's quiet here. Too quiet.
@endnode
```

This section describes the language itself:

- **[Text](text.md)**: narration, interpolation, and quoted strings.
- **[Dialogue](dialogue.md)**: lines spoken by characters.
- **[Statements](statements.md)**: variables, jumps, detours, and game functions.
- **[Conditions and randomness](blocks.md)**: `@if`, `@match`, and `@random`.
- **[Options](options.md)**: choices offered to the player.
- **[Expressions](expressions.md)**: values, operators, types, and built-in functions.
- **[Declarations (@env)](env.md)**: variables, characters, pools, slots, meta keys, and functions.
- **[Storylets and meta](meta.md)**: node metadata, pools, and `@draw`.
- **[Limitations](limitations.md)**: what the language doesn't support yet.

## Files

A project keeps its sources in a `src` folder, in any number of `.wvl` files and subfolders. Files are read as UTF-8. Each file holds any number of `@env` blocks and `@node` blocks, in any order.

All files of a project share one set of names: a variable declared in one file can be used in every other, and a node in one file can jump to a node in another.

## Nodes

A node is a named piece of dialogue. Everything the player sees and does happens inside one:

```
@node CaveEntrance
You stand at the mouth of a cave.
@endnode
```

When the game starts a node, its statements run from top to bottom. A line of text pauses until the player continues. When the node runs out of statements, the dialogue returns to whatever [detoured](statements.md#detour) into it, or finishes if nothing did.

A node can start with one [`@meta` block](meta.md) right after its `@node` line.

## Names

Node ids, variables, characters, pools, slots, meta keys and functions are all names. A name starts with a letter or `_`, followed by letters, digits or `_`. Names are case-sensitive.

Every name is unique across the whole project, whatever it names: a node can't share its name with a variable, and two files can't declare the same variable. A duplicate is an error that points to both places.

## Keywords

Everything that starts with `@` is a Weavly keyword, such as `@node`, `@if` or `@jump`. An unknown keyword is an error, and the compiler suggests a close one if there is one.

Blocks end with their own closing keyword: `@endnode`, `@endif`, `@endoptions`, `@endmatch`, `@endrandom`, `@endmeta` and `@endenv`.

## Comments

`#` starts a comment that runs to the end of the line. A comment can sit on its own line or at the end of a statement:

```
# The guard only talks once.
@node Guard
@set guard_met = true  # remembered for later visits
Halt!
@endnode
```

On narration and dialogue lines, `#` is part of the text, so `Prices start at #5.` shows the `#`. See [Text](text.md#hash-signs).

## Indentation and blank lines

Indentation and blank lines have no meaning: blocks end with their closing keyword, not with indentation. Indent however reads best. The examples in these docs indent block bodies by four spaces.

## Naming convention

Weavly recommends, but never enforces, a convention modelled on GDScript:

- Nodes and characters in PascalCase: `@jump MarketSquare`, `Anna: Hello.`
- Variables, pools, slots, meta keys and functions in snake_case: `gold`, `camp_actions`, `play_sound`.

Because every name shares one namespace, the convention also makes it easy to tell a node from a variable at a glance.
