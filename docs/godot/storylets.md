# Storylets and pools

Scripts pick storylets with [`@draw`](../language/meta.md#draw) and [`pool(...)` options](../language/options.md#pool). The game can ask the same questions from GDScript, for example to show the events available on a map, or to start a random encounter.

## Starting a storylet

`draw()` picks the first eligible node from the pools and starts a dialogue with it:

```gdscript
func _on_camp_entered() -> void:
	if not engine.draw(["camp_events"]):
		$Hint.text = "Nothing happens tonight."
```

It returns `false` when no node is eligible, and does nothing while a dialogue is running.

## Listing a pool

`list_pool()` returns the ids of the nodes a pool offers right now, in the order [described for scripts](../language/meta.md#how-nodes-are-picked):

```gdscript
var ids: Array[String] = engine.list_pool(["camp_events", "night_events"], 3)
```

| Parameter | Default | Meaning |
|---|---|---|
| `pools` | | the pool names |
| `limit` | `-1` | the most nodes to return; `-1` for all |
| `shuffle` | `true` | order nodes of equal priority at random by weight; otherwise in source order |
| `locked` | `WeavlyEngine.Locked.SHOW` | how nodes that would show locked count: `SHOW` toward the limit, `EXTRA` on top of it, `HIDE` not at all |

Listing updates the [skip counts](../language/meta.md#skip-count), like a script listing the pool would. `peek_pool()` takes the same parameters and returns the same ids without changing skip counts or the random state, for previews such as the [debug overlay](ui.md#debug-overlay).

## Nodes as options

`get_option()` returns a node as an option, the way an `@options` block would offer it, or `null` when the node would be hidden:

```gdscript
func _show_events() -> void:
	for node_id in engine.list_pool(["camp_events"], 3):
		var option := engine.get_option(node_id)
		if option == null:
			continue
		var button := Button.new()
		button.text = option.text
		button.disabled = not option.is_choosable()
		button.pressed.connect(engine.choose.bind(option))
		$Events.add_child(button)
```

The option needs a `label` in the node's `@meta`. `choose(option)` starts a dialogue with the node, and accepts the option as long as the game keeps a reference to it.

## Meta values

`get_node_meta()` reads a node's [meta value](../language/meta.md#reading-meta-values), or the key's default if the node doesn't set it:

```gdscript
var cost: float = engine.get_node_meta("RentRoom", "cost")
```

It evaluates the value at the moment it's called. Like `peek_pool()`, it leaves the random state as it was.
