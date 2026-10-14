# Options

An `@options` block offers the player a choice:

```wvl
@options
@option "Open the door"
    The door creaks open.
    @jump Hall
@option [has_key] "Unlock the chest": @detour Chest
@option "Leave": @finish
@endoptions
```

The dialogue pauses until the player picks one. The chosen option then runs like a [detour](statements.md#detour): unless it jumps or finishes, the dialogue continues after `@endoptions`.

If a block has nothing to show, for example because every condition is false, the dialogue continues after `@endoptions` right away.

## Three kinds of options

Every option is a node. A block offers nodes in three ways, and shows them in the order they're written:

```wvl
@options
@option "Wait": You wait for a while.
@option node(HackTerminal)
@option pool(camp_actions, limit: 3)
@endoptions
```

### Inline options

`@option "text"` writes the option in place. The text is its label, and an optional condition in `[...]` decides whether it's shown. The action is [inline or a body](blocks.md#actions), as in other blocks.

An inline option is an anonymous node: it has no id, no `@meta`, and no visit count. Inside it, `visited()`, `visit_count()`, `skip_count()` without an argument and `.key` refer to the node the `@options` block is in.

### `node(...)`

`@option node(Id)` offers an existing node. The node needs a `label` in its [`@meta`](#option-keys), which is the text the player sees, and its `when` decides whether it's shown:

```wvl
@node HackTerminal
@meta
label: "Hack the terminal"
when: has_tools
@endmeta
The screen flickers to life.
@endnode
```

To offer several nodes, write one `@option node(...)` line each. A `node` variable works too: `@option node(next_step)`.

### `pool(...)`

`@option pool(...)` offers the nodes picked from one or more [pools](meta.md), as if the pools were listed in its place. Every node in those pools needs a `label`.

Pools come first, then named parameters:

```wvl
@option pool(camp_actions, night_actions, limit: 3, shuffle: false, locked: hide)
```

| Parameter | Value | Default |
|---|---|---|
| `limit` | the most options to offer, a number expression | no limit |
| `shuffle` | whether nodes of equal priority are ordered at random, by weight. Otherwise they keep their source order. | `true` |
| `locked` | how [locked options](#locked-options) count: `show` (shown, and they count toward `limit`), `extra` (shown, but only choosable ones count), or `hide` (left out) | `show` |

See [Storylets and meta](meta.md#how-nodes-are-picked) for how nodes are picked from a pool.

## Option keys

These [meta keys](meta.md) describe a node as an option:

| Key | Value |
|---|---|
| `label` | the option text |
| `available` | a bool; when false, the option is shown but locked |
| `label_unavailable` | the text of the locked option when `available` is false |
| `label_teaser` | the text of the locked option when `when` is false |

The label keys take any string expression, such as `label: "Buy for {price} gold"` or `label: shop_name`.

## Locked options

A locked option is shown but can't be chosen. It's how a choice the player can't take yet stays visible:

```wvl
@node BuySword
@meta
label: "Buy the sword"
available: gold >= 50
label_unavailable: "Buy the sword (50 gold)"
when: visited(Smithy)
label_teaser: "???"
@endmeta
@decrease gold 50
@endnode
```

| `when` | `available` | The option is |
|---|---|---|
| true | true | shown with `label`, choosable |
| true | false | shown locked with `label_unavailable`, or hidden without it |
| false | either | shown locked with `label_teaser`, or hidden without it |

## When options are evaluated

Options are evaluated once, when the block is shown: which ones are offered, their order, their labels, and whether they're locked. They don't change while they're on screen, even if a variable changes.

A node option also keeps the meta values it had when it was offered. When the player chooses it, the node reads those values, so a label like `"Rent a room ({.cost} gold)"` always matches the `.cost` the node then uses.

## `@continue`

`@continue` is a block with a single option, for a pause the player clicks through:

```wvl
@continue "Onward"
@continue "Follow her": @jump Alley
```

It takes an inline action but no body.
