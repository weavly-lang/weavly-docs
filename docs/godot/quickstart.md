# Quick start

This page plays a dialogue in a Godot scene, first with a starter UI and then with your own. It assumes the addon is [installed](index.md#installation).

## Write the dialogue

In a terminal, in your Godot project's folder, create a Weavly project in `dialogue`:

```bash
weavly init dialogue
```

Back in Godot, open `res://dialogue/src/nodes.wvl` from the FileSystem dock. It opens in the **Weavly** screen at the top of the editor. Replace its contents with:

```wvl
@env
character Guide
@endenv

@node FirstNode
Guide: Welcome to the village.
Guide: Can I help you?

@options
@option "Where's the inn?": Guide: Down the road, on the left.
@option "No, thanks.": Guide: Enjoy your stay.
@endoptions
@endnode
```

Click **Compile** in the toolbar. The status shows *Build successful*, and `res://dialogue/build` now holds the compiled dialogue.

## Play it with a starter UI

1. Create a scene with a `Control` root.
2. Instance `res://addons/weavly/runtime/weavly_engine.tscn` as a child. This is the `WeavlyEngine` node that runs the dialogue.
3. Instance `res://addons/weavly/ui/novel/weavly_novel_ui.tscn` as another child, and set its **Engine** to the engine node in the Inspector.
4. Attach a script to the root that starts the dialogue:

    ```gdscript
    extends Control

    @onready var engine: WeavlyEngine = $WeavlyEngine


    func _ready() -> void:
    	engine.start("FirstNode")
    ```

Run the scene. The guide's lines appear in a textbox; click or press Enter to continue, and pick an option to answer.

## Play it with your own UI

The engine doesn't draw anything. It sends signals, and your game shows the dialogue however it likes. Replace the novel UI with a `Label` called `Text` and a `VBoxContainer` called `Choices`, and use this script:

```gdscript
extends Control

@onready var engine: WeavlyEngine = $WeavlyEngine
@onready var text: Label = $Text
@onready var choices: VBoxContainer = $Choices


func _ready() -> void:
	engine.line_reached.connect(_on_line_reached)
	engine.options_offered.connect(_on_options_offered)
	engine.finished_dialogue.connect(_on_finished_dialogue)
	engine.start("FirstNode")


func _on_line_reached(line: WeavlyModel.LineStatement) -> void:
	if line is WeavlyModel.CharacterLine:
		text.text = "%s: %s" % [line.name, line.text]
	else:
		text.text = line.text


func _on_options_offered(options: Array[WeavlyModel.Option]) -> void:
	for option in options:
		var button := Button.new()
		button.text = option.text
		button.disabled = not option.is_choosable()
		button.pressed.connect(_on_option_pressed.bind(option))
		choices.add_child(button)


func _on_option_pressed(option: WeavlyModel.Option) -> void:
	for button in choices.get_children():
		button.queue_free()
	engine.choose(option)


func _on_finished_dialogue() -> void:
	text.text = ""


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		engine.next()
```

- A line pauses the dialogue. `next()` continues it.
- Options pause it until `choose()` is called with one of them.
- `next()` does nothing while options are waiting, so pressing Enter can't skip a choice.

## Next steps

- [Running dialogue](engine.md): everything the engine signals and does.
- [Variables and functions](game-data.md): share game state with your scripts.
- [Starter UIs](ui.md): the other ready-made UIs.
