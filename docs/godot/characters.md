# Characters

A character declared in a script, like `character Anna`, has only an id. The game decides what the player sees as its name.

## Character resources

A `WeavlyCharacter` resource gives a character its display name:

1. Create a folder for characters, for example `res://characters`.
2. In it, create a new resource of type `WeavlyCharacter` for each character, saved as `.tres`.
3. Set its `id` to the character's id in the script, `Anna`, and its `display_name` to what the player sees, `Anna Weber`.
4. Set the engine's `character_path` to the folder. The engine loads every `WeavlyCharacter` resource in it, subfolders included.

Lines then carry both: `line.character` is the id and `line.name` the display name. See [Lines](engine.md#lines).

A character without a resource, or with an empty `display_name`, shows its id. With a `character_path` set, the engine warns once for each such character.

The [starter UIs](ui.md#characters) have their own resource types that add a name color, an avatar or a bubble color.

## Changing names during play

Display names are resolved each time a line runs, through the character service. To show `???` until the player learns a name, replace that service with a script that extends the default one:

```gdscript
extends WeavlyDefaultCharacterService


func get_display_name(id: String) -> String:
	if id == "Stranger" and not engine.get_variable("knows_stranger"):
		return "???"
	return super(id)
```

Add the script to the engine's `custom_services`, see [Custom services](services.md).

Every place a character becomes text goes through this: the speaker of a line, and `{Stranger}` in a line or a string. A line keeps the name it was shown with.
