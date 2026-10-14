# Variables and functions

Scripts and the game share state through variables, and the game gives scripts new abilities through functions. Both are declared in [`@env`](../language/env.md).

## Variables

`get_variable()` and `set_variable()` read and change any declared variable:

```gdscript
var gold: float = engine.get_variable("gold")
engine.set_variable("gold", gold + 10)
```

Values have these Godot types:

| Weavly type | Godot type |
|---|---|
| `number` | `float` (an `int` is accepted when setting) |
| `string` | `String` |
| `bool` | `bool` |
| `node`, `pool`, `slot`, `character` | `String`, the name |

`set_variable()` checks the value against the declaration. A value of the wrong type, or a name that doesn't exist, is reported as an [error](engine.md#errors) and ignored. A number outside its [range](../language/env.md#ranges) is kept at the nearest end.

`variable_changed(id, value, old_value)` fires whenever a variable gets a different value, from the script or the game, which is a good place to update a HUD:

```gdscript
func _ready() -> void:
	engine.variable_changed.connect(_on_variable_changed)


func _on_variable_changed(id: String, value: Variant, _old_value: Variant) -> void:
	if id == "gold":
		$GoldLabel.text = str(int(value))
```

### Variables the game owns

A value that belongs to the game, like the player's level, is declared `extern var`:

```wvl
@env
extern var player_level: number
@endenv
```

The game sets it before a script reads it, typically right after the engine is ready:

```gdscript
func _ready() -> void:
	engine.set_variable("player_level", Player.level)
```

Scripts can read and change extern variables like any other. The engine doesn't [save](saving.md) them: the game saves them with its own data. A script that reads an extern variable the game never set gets a runtime error.

## Functions

A function declared in `@env` is provided by the game with `register_function()`:

```wvl
@env
func has_item(item: string): bool
func play_sound(name: string, volume: number)
@endenv
```

```gdscript
func _ready() -> void:
	engine.register_function("has_item", _has_item)
	engine.register_function("play_sound", _play_sound)


func _has_item(item: String) -> bool:
	return Inventory.has(item)


func _play_sound(sound_name: String, volume: float) -> void:
	$Audio.stream = load("res://sounds/%s.ogg" % sound_name)
	$Audio.volume_db = linear_to_db(volume)
	$Audio.play()
```

- The callable gets the arguments in declaration order, with the types from the table above. Declare number parameters as `float`.
- Its argument count must match the declaration, or `register_function()` refuses it with an error.
- A function with a return type must return a value of that type. The engine checks the result and reports a wrong one.
- Register every function before the first dialogue starts. The engine reports each declared function without a callable once, when the game first uses it.

### Where functions run

A function in an expression, such as `@if has_item("lantern")`, may run any number of times: when options are offered, when pools are listed, and when the debug overlay refreshes. It should only return a value.

A function called with `@do` runs exactly once, at its place in the script. That's where it may change the game. To make the dialogue wait for it, for example while an animation plays, use `hold()` and `release()`:

```gdscript
func _shake_screen(strength: float) -> void:
	engine.hold()
	await $Camera.shake(strength)
	engine.release()
```

### `var` parameters

A [`var` parameter](../language/env.md#passing-a-variable) passes a variable instead of its value. The callable gets the variable's name as a `String`, and reads and changes it through the engine:

```wvl
@env
var gold: number = 20
func add_loot(target: var number, amount: number)
@endenv

@node Chest
@do add_loot(var gold, 5)
@endnode
```

```gdscript
func _add_loot(target: String, amount: float) -> void:
	var bonus := 2.0 if Player.lucky else 1.0
	engine.set_variable(target, engine.get_variable(target) + amount * bonus)
```
