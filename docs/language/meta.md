# Storylets and meta

A node can describe itself with a `@meta` block. Meta values let the game, and the script, ask questions about a node without running it: is it available, what does it cost, which group does it belong to.

The main use is **storylets**: nodes that join a pool, and that the game or script picks from at runtime based on their conditions and priorities. Instead of wiring every event by hand, you write many small nodes and let the pool decide which one fits right now.

## `@meta`

The `@meta` block comes right after the `@node` line and holds `key: value` entries:

```
@node FindTreasure
@meta
pool: cave_events
slot: cave_reward
when: luck > 5
priority: 1
weight: 1 + skip_count()
once: true
@endmeta
You find a chest full of gold.
@endnode
```

A node has at most one `@meta` block. Unknown and duplicate keys are errors, and the compiler suggests a close key if there is one.

## Built-in keys

| Key | Value | Default |
|---|---|---|
| `pool` | one or more pool names, separated by commas | none |
| `slot` | one or more slot names, separated by commas | none |
| `when` | a bool; the node is eligible only while it's true | `true` |
| `priority` | a number; higher goes first | `0` |
| `weight` | a number; how likely the node is among nodes of equal priority | `1` |
| `once` | `true` or `false`; `true` makes the node ineligible once it was visited | `false` |
| `label`, `available`, `label_unavailable`, `label_teaser` | see [Option keys](options.md#option-keys) | |

`once: true` is a shortcut for adding `not visited()` to `when`.

`pool` and `slot` take names only, not variables: which pools a node is in has to be known when the project is built.

## How nodes are picked

When a pool is listed, by [`@draw`](#draw), a [`pool(...)` option](options.md#pool) or the game:

1. Every node in the given pools whose `when` is true is a candidate. A node in several of the pools counts once.
2. Candidates are ordered by `priority`, highest first.
3. Candidates with equal priority are shuffled, with a higher `weight` making a node more likely to come first. Nodes with a weight of 0 or less are left out. A `pool(...)` option with `shuffle: false` keeps them in source order instead.
4. Nodes are taken from the top. Once a node is taken, other nodes that share one of its slots are skipped.

A fallback is a node in the pool with a low priority and no `when`: it's picked only when nothing better is eligible.

```
@node QuietNight
@meta
pool: camp_events
priority: -1
@endmeta
The night passes without incident.
@endnode
```

### Slots

Nodes that share a slot exclude each other: at most one of them is taken per listing. Use slots for nodes that are alternatives of each other, such as three different weather events where only one should come up.

### Skip count

`skip_count()` counts how often a node was eligible when its pool was listed but wasn't taken. It resets to 0 when the node is taken. A weight like `1 + skip_count()` makes a node more likely each time it's passed over.

## `@draw`

`@draw` takes the first node of the listing and runs it like a [detour](statements.md#detour):

```
@node Camp
You set up camp for the night.
@draw camp_events
You wake at dawn.
@endnode
```

If no node is eligible, nothing is drawn and the dialogue continues.

## Custom keys

A [declared meta key](env.md#meta-keys) can be set on any node, with a value of the declared type:

```
@env
meta cost: number = 0
@endenv

@node RentRoom
@meta
cost: 2 + visit_count() * 2
label: "Rent a room ({.cost} gold)"
@endmeta
@decrease gold .cost
@endnode
```

Values are expressions, evaluated each time they're read. A node that doesn't set the key has its default.

## Reading meta values

`.key` reads a value of the current node, and `Node.key` one of another node:

```
@if gold >= RentRoom.cost: You can afford a room.
```

Readable keys are custom keys and `when`, `priority`, `weight` and `available`. `pool`, `slot` and `once` can't be read.

Inside an [inline option](options.md#inline-options), `.key` means the node the `@options` block is in.

A meta value that reads itself, directly or through other meta values, is an error, for example `meta key 'cost' reads itself: A.cost -> B.cost -> A.cost`.
