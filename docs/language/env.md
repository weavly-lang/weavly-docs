# Declarations (`@env`)

Everything a script uses besides nodes is declared in an `@env` block:

```wvl
@env
var score: number(0, 100) = 0
var player_name: string = "Hero"
var brave: bool = true
var next_room: node = Hall
extern var reputation: number
character Anna
pool camp_events
slot weather
meta cost: number = 1
func trust(from: character, to: character): number
func play_sound(name: string, volume: number)
@endenv
```

Each line starts with its kind. A file can have several `@env` blocks, and the build merges the declarations of every file in the project, so each name is declared once and used everywhere. Names share one namespace with node ids, see [Names](index.md#names).

## Variables

`var name: type = default` declares a variable:

| Type | Holds | Default without `= ...` |
|---|---|---|
| `number` | a number | `0` |
| `string` | text | `""` |
| `bool` | `true` or `false` | `false` |
| `node`, `pool`, `slot`, `character` | a node, pool, slot or character | none, a default is required |

```wvl
@env
var gold: number = 20
var visited_city: bool
var companion: character = Anna
@endenv
```

Defaults are constants: a number, a quoted string without `{}`, `true` or `false`, or a name. A name must exist and have the right kind.

### Ranges

A `number` can have a range, `(min, max)`. Either side can be left out:

```wvl
@env
var health: number(0, 100) = 100
var debt: number(0,) = 0
var temperature: number(, 40) = 20
@endenv
```

The default must fit the range. While the game runs, a value outside the range is kept at the nearest end, so `@decrease health 500` leaves `health` at `0`.

### Variables the game owns

`extern var` declares a variable that the game sets, not the script:

```wvl
@env
extern var player_level: number
extern var player_class: string
@endenv
```

It has no default and no range. Scripts read and change it like any other variable, and the game must give it a value before a script reads it. In Godot, see [Variables and functions](../godot/game-data.md).

## Characters

`character Name` declares a character that can [speak](dialogue.md):

```wvl
@env
character Anna
character Narrator
@endenv
```

The declaration holds only the id. The game owns the [display name](dialogue.md#display-names).

## Pools and slots

`pool name` and `slot name` declare the pools and slots that [storylets](meta.md) join:

```wvl
@env
pool camp_events
slot weather
@endenv
```

## Meta keys

`meta name: type = default` declares a custom [meta key](meta.md#custom-keys) that nodes can set in their `@meta` block:

```wvl
@env
meta cost: number = 1
meta mood: string = "calm"
@endenv
```

Defaults work like those of variables, but meta keys take no range. A node that doesn't set the key has the default. Built-in key names, such as `when` or `label`, can't be declared.

## Functions

`func name(parameter: type, ...)` declares a function the game provides. A return type after the parentheses makes it usable in expressions:

```wvl
@env
func trust(from: character, to: character): number
func has_item(item: string): bool
func play_sound(name: string, volume: number)
@endenv
```

Parameter names are required and must differ. A function can't have the name of a built-in function.

There are two ways to call a function:

- **In an expression**, if it has a return type: `@if has_item("lantern")`.
- **As a statement** with [`@do`](statements.md#do), whether or not it has a return type. The result is dropped: `@do play_sound("door", 1)`.

A call passes exactly the declared parameters. There are no optional or variadic parameters.

!!! warning "Functions in expressions may run more than once"
    The game evaluates expressions whenever it needs their value: options refresh while they're shown, and pools check their nodes' conditions each time they're listed. A function in an expression can run any number of times, so it should only return a value. Anything that changes the game belongs in a `@do`, which runs exactly once.

### Passing a variable

A parameter of type `var <type>` takes a variable instead of its value, so the game can change it:

```wvl
@env
var gold: number = 20
func add_loot(target: var number, amount: number)
@endenv

@node Chest
@do add_loot(var gold, 5)
@endnode
```

The argument is written with `var` too. It must be a variable of exactly that type, `extern` variables included. Its range doesn't matter. Any type works, but only for parameters: there are no `var` return types.

Built-in statements take the variable without `var`, because the keyword already says it changes: `@set gold = 5`, `@increase gold`.
