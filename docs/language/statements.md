# Statements

Statements are the lines of a node that start with a keyword. Each takes one line. Blocks that hold other statements are covered in [Conditions and randomness](blocks.md) and [Options](options.md).

## Variables

### `@set`

`@set` gives a [variable](env.md#variables) a new value:

```wvl
@set gold = 10
@set greeting = "Hello, {player_name}!"
@set has_key = gold > 5 and not cursed
```

The value must have the variable's type. Setting a number outside its [range](env.md#ranges) keeps it at the nearest end of the range.

### `@increase` and `@decrease`

`@increase` and `@decrease` add to or take from a number variable. The amount defaults to 1 and can be any number expression:

```wvl
@increase visits
@increase gold 10
@decrease health damage * 2
```

`@increase gold 10` is the same as `@set gold = gold + 10`.

## Flow

### `@jump`

`@jump` moves to another node for good:

```wvl
@jump Village
```

Everything the dialogue was going to return to is dropped: after a `@jump`, the dialogue finishes when the new node ends, even if the `@jump` happened inside a [detour](#detour).

### `@detour`

`@detour` runs another node, then continues after the `@detour` once that node ends:

```wvl
@node Shop
@detour Greeting
What would you like to buy?
@endnode

@node Greeting
Welcome, traveller.
@endnode
```

Detours can be nested: a detoured node can detour again. Options, `@draw` and `@random` cases run what they pick the same way.

There's no `@return`: a detour returns when its node runs out of statements.

### `@draw`

`@draw` picks one node from one or more [pools](meta.md) and runs it like a detour:

```wvl
@draw camp_events
@draw forest_events, weather_events
```

If no node in the pools is eligible, nothing happens and the dialogue continues. See [Storylets and meta](meta.md#draw) for how the node is picked.

### `@finish`

`@finish` ends the whole dialogue at once, even inside a detour:

```wvl
@if health <= 0: @finish
```

A dialogue also finishes when a node ends and there's no detour to return to.

### Variables as targets

`@jump`, `@detour` and `@draw` take a name or a variable of the matching type. A `node` variable lets the script decide later where to go:

```wvl
@env
var next_room: node = Hall
@endenv

@node Corridor
@jump next_room
@endnode
```

`@draw` takes `pool` variables, mixed with pool names.

## Game functions

### `@do`

`@do` calls a [function the game provides](env.md#functions) and ignores its result:

```wvl
@do play_sound("door_creak", 0.8)
@do shake_screen(2)
```

The parentheses are required, even without arguments: `@do save_game()`.

`@do` runs exactly once, at its place in the script, so it's the place for anything that changes the game. A function called inside an expression may run any number of times, see [Functions](env.md#functions).

## Visits

A node counts as visited when it ends: when it runs out of statements, when a `@jump` leaves it, or when the dialogue finishes. Inside a node's first visit, `visited()` is still `false`. See [Node functions](expressions.md#node-functions).
