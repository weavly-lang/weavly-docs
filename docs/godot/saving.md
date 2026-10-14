# Saving and loading

The engine's state is a `Dictionary` that converts to JSON, so it fits into any save system.

## Saving

`get_state()` returns everything the dialogue needs to continue later:

```gdscript
func save_game() -> void:
	var save := {
		"dialogue": engine.get_state(),
		"player_level": Player.level,
	}
	var file := FileAccess.open("user://save.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(save))
```

A state holds:

- the values of the script's variables, except `extern` ones, which the game [saves itself](game-data.md#variables-the-game-owns)
- how often each node was visited and skipped
- the random generator's state
- during a dialogue, the node that's running

During a dialogue, the state is the one from when the current node started. Loading it replays that node from its beginning, so a save in the middle of a node never resumes halfway through it.

## Loading

`set_state()` ends any running dialogue and restores the state:

```gdscript
func load_game() -> void:
	var save = JSON.parse_string(FileAccess.get_file_as_string("user://save.json"))
	if save is not Dictionary:
		return
	engine.set_state(save["dialogue"])
	engine.set_variable("player_level", save["player_level"])
```

The engine emits `state_loaded`. If the state was saved during a dialogue, the engine then starts its node again.

`reset_state()` goes back to the state the engine had after loading the dialogue, for a new game. Extern variables keep their values in both cases.

## Old saves

Saves outlive script changes. When a state is loaded:

- A variable that no longer exists is skipped, with a warning.
- A value that no longer fits its variable's type is replaced by the default, with a warning. A number outside a new range is kept at its nearest end.
- Counts for a node that no longer exists are skipped.
- If the running node no longer exists, the state loads without starting a dialogue, with an error.

A state from a different addon version with an incompatible format is refused with an error, and nothing is loaded.
