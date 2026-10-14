# Running dialogue

`WeavlyEngine` is the node that runs dialogue. Instance `res://addons/weavly/runtime/weavly_engine.tscn`, or add it as an autoload to keep one engine for the whole game. It loads the compiled dialogue when it enters the tree.

## Settings

| Export | Default | Meaning |
|---|---|---|
| `dialogue_path` | `res://dialogue/build` | the folder with the compiled dialogue |
| `random_seed` | `0` | the seed for `@random`, `random()` and pool shuffling; `0` picks a new seed on every run |
| `character_path` | empty | a folder of [character resources](characters.md); empty if the game has none |
| `max_node_entries_per_step` | `10000` | how many nodes the dialogue may enter without pausing before it stops, which catches jump cycles |
| `max_detour_depth` | `64` | how many nodes can run at once through detours, options and `@draw` |
| `custom_services` | empty | scripts that replace parts of the engine, see [Custom services](services.md) |

## The flow of a dialogue

```gdscript
engine.start("FirstNode")
```

`start()` runs the node until it reaches something the player has to see:

- **A line.** The engine emits `line_reached` and waits. Call `next()` to continue.
- **Options.** The engine emits `options_offered` and waits. Call `choose()` with one of the options.
- **The end.** When the dialogue finishes, the engine emits `finished_dialogue`.

`next()` does nothing while choosable options are waiting. If every offered option is locked, `next()` continues past the block, so the dialogue doesn't get stuck.

Only one dialogue runs at a time. `start()` while a dialogue is running is ignored with a warning; call `finish()` first to end it.

## Signals

| Signal | When |
|---|---|
| `started_dialogue()` | a dialogue starts |
| `entered_node(node_id: String)` | a node starts running |
| `left_node(node_id: String)` | a node ends, counted as a visit |
| `line_reached(line: WeavlyModel.LineStatement)` | a line is shown, its text filled in |
| `options_offered(options: Array[WeavlyModel.Option])` | options wait for a choice |
| `option_chosen(option: WeavlyModel.Option)` | an option was chosen |
| `statement_reached(statement: WeavlyModel.Statement)` | any statement is about to run |
| `variable_changed(id: String, value: Variant, old_value: Variant)` | a variable got a different value |
| `finished_dialogue()` | the dialogue ended |
| `state_loaded()` | a saved state was [loaded](saving.md) |
| `runtime_error(message: String, source: String, line: int)` | something went wrong while running, see [Errors](#errors) |

## Lines

`line_reached` passes a `WeavlyModel.LineStatement`, either a `NarrationLine` or a `CharacterLine`:

| Property | On | Holds |
|---|---|---|
| `text` | both | the line's text, interpolation filled in |
| `character` | `CharacterLine` | the speaking character's id, empty for a one-off speaker |
| `name` | `CharacterLine` | the speaker's display name, see [Characters](characters.md) |
| `source`, `line` | both | the `.wvl` file, relative to `src/`, and the line number |

The text and name are filled in when the line runs, so a backlog that keeps the line objects keeps them as they were shown.

## Options

`options_offered` passes the options in the order they're shown. Each `WeavlyModel.Option` has:

| Property or method | Holds |
|---|---|
| `text` | the label to show |
| `is_choosable()` | `false` for a [locked option](../language/options.md#locked-options) |
| `state` | `Option.State.AVAILABLE`, `UNAVAILABLE` (locked by `available`) or `TEASER` (locked by `when`) |
| `node_id` | the offered node's id, empty for an inline option |

Show locked options disabled: `choose()` refuses them. `can_choose(option)` tells whether `choose()` would take an option, and `get_pending_options()` returns the options the dialogue waits on.

Options are fixed when they're offered. To reflect a change, offer them again.

## Waiting for the game

`hold()` pauses the dialogue until a matching `release()`, for example while an animation plays:

```gdscript
func _on_entered_node(node_id: String) -> void:
	if node_id == "Earthquake":
		engine.hold()
		await $Camera.shake()
		engine.release()
```

Holds stack: the dialogue continues after the last `release()`. A line on screen keeps waiting for `next()` either way. In a [game function](game-data.md#functions) called by `@do`, `hold()` makes the dialogue wait for the function.

## Rendering a whole node

For UIs that show a node at once, such as a page of a book or a Twine-style passage, `render()` runs a node without pausing and returns what it showed:

```gdscript
var statements := engine.render("Library")
for statement in statements:
	if statement is WeavlyModel.LineStatement:
		_add_paragraph(statement.text)
	elif statement is WeavlyModel.OptionBlock:
		_add_links(statement.options)
```

The result holds the node's lines, its `@do` statements (with the evaluated arguments in `values`) and its option blocks (with the offered options in `options`), in order.

Rendering is playing: variables change, `@do` functions are called, and visits count. Choose a rendered option with `render_option(option)` to render what it leads to, or with `choose(option)` to play it as a normal dialogue. Rendered options stay choosable as long as the game keeps a reference to them.

## Errors

Mistakes the compiler can't catch, such as an `extern var` the game never set or a function that returns the wrong type, are reported while the game runs:

```text
shop.wvl:12: error: Variable 'player_gold' is declared extern but was never defined.
```

The engine prints the error, emits `runtime_error` with the message, file and line, and carries on as well as it can. A missing node or a jump cycle finishes the dialogue. The [debug overlay](ui.md#debug-overlay) lists every runtime error.
