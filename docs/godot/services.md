# Custom services

The engine delegates parts of its work to services. Each one can be replaced to change how the engine behaves, without changing the addon.

| Service | Decides | Default |
|---|---|---|
| `WeavlyCharacterService` | characters and their display names | loads [character resources](characters.md) |
| `WeavlyCountService` | visit and skip counts | keeps them in memory and in saves |
| `WeavlyFunctionService` | calling [game functions](game-data.md#functions) | calls the registered callables |
| `WeavlyLineService` | whether a line waits for `next()` | every line waits |
| `WeavlyVariableService` | where variable values are stored | keeps them in memory and in saves |

## Replacing a service

1. Write a script that extends a service, or its default implementation (`WeavlyDefaultCharacterService`, `WeavlyDefaultCountService`, `WeavlyDefaultFunctionService`, `WeavlyDefaultLineService`, `WeavlyDefaultVariableService`). Extending the default lets you change one method and keep the rest.
2. Add the script to the engine's `custom_services` in the Inspector.

The engine creates its services when it enters the tree, so set `custom_services` before that. Each service can be replaced once: a second script for the same service is reported and ignored.

Inside a service, `engine` is the engine it belongs to.

## Lines that don't wait

For barks or ambient chatter that play on their own, a line service can tell the engine not to wait:

```gdscript
extends WeavlyLineService


func waits(line: WeavlyModel.LineStatement) -> bool:
	return false
```

The engine still emits `line_reached` for every line, but runs on to the next options or the end of the dialogue without waiting for `next()`.

## Hidden names

See [Changing names during play](characters.md#changing-names-during-play) for a character service that shows `???` until the player learns a name.

## Keeping state elsewhere

A variable or count service can keep its values in the game's own data instead, for example in an autoload that the save system already writes:

```gdscript
extends WeavlyVariableService


func has(id: String) -> bool:
	return GameState.dialogue_variables.has(id)


func get_value(id: String) -> Variant:
	return GameState.dialogue_variables.get(id)


func set_value(id: String, value: Variant) -> void:
	GameState.dialogue_variables[id] = value
```

The engine checks every value against its declaration before it calls `set_value()`, and when it reads one back.

## Services and saves

A service that keeps state returns it from `get_state()` and restores it in `set_state()`. The engine puts what `get_state()` returns into its own [state](saving.md), so it's saved and loaded with the rest. Return only values that convert to JSON. A service whose state lives elsewhere, like the example above, returns an empty `Dictionary`, which is the default.
