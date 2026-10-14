# Conditions and randomness

## Actions

Every case of a block takes an action, written in one of two ways:

- **Inline**: a colon and one statement on the same line.
- **As a body**: any number of statements on the following lines, up to the next case or the end of the block.

```
@if gold > 10
    You feel rich.
    @set mood = "smug"
@elif gold > 0: You have a little.
@else: @jump Broke
@endif
```

The inline statement can be a line of text or any [statement](statements.md), but not another block.

Bodies can hold any statements, including other blocks, nested as deep as needed.

## `@if`

`@if` runs the first case whose condition is true. `@elif` adds more cases, and `@else` runs when no condition is true. Both are optional.

```
@if reputation >= 50
    The guards salute you.
@elif reputation >= 0
    The guards ignore you.
@else
    The guards reach for their swords.
@endif
```

An `@if` with an inline action is complete on its line. It takes no `@elif`, `@else` or `@endif`:

```
@if scared: @do shake(2)
@if met_guide: Guide: You again.
```

So an `@else` always belongs to an `@if` with a body.

## `@match`

`@match` checks a list of `@when` cases:

```
@match all
@when has_sword: You draw your sword.
@when has_shield: You raise your shield.
@when allies > 0: Your allies close ranks.
@endmatch
```

The modifier after `@match` decides which cases run:

| Modifier | Runs |
|---|---|
| `first` (default) | the first case whose condition is true |
| `last` | the last case whose condition is true |
| `all` | every case whose condition is true, in order |

If no condition is true, nothing runs. `@match first` works like `@if` without `@else`. `@match last` is handy for a list ordered from weakest to strongest:

```
@match last
@when level >= 1: You're a novice.
@when level >= 5: You're an adept.
@when level >= 10: You're a master.
@endmatch
```

## `@random`

`@random` runs one of its `@case`s at random:

```
@random
@case: You find nothing.
@case 3: You find a coin.
@case [lucky] 2: You find a ring.
@endrandom
```

Each case can have:

- **A condition** in `[...]`. A case whose condition is false can't be picked. Without one, the case can always be picked.
- **A weight**, a number expression. A case with weight 3 is three times as likely as one with weight 1. The default is 1.

In the example, when `lucky` is true the coin has a 3 in 6 chance. When it's false, the ring is out and the coin has a 3 in 4 chance.

Cases with a weight of 0 or less are never picked. If no case can be picked, nothing runs and the dialogue continues.

Weights are evaluated each time the block runs, so they can change during play:

```
@random
@case 1 + visit_count(): Business as usual.
@case danger: Something feels wrong.
@endrandom
```

## Empty blocks

`@if`, `@match`, `@random` and [`@options`](options.md) need at least one case. An empty block is an error.
