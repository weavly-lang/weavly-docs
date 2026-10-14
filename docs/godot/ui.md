# Starter UIs

The addon comes with ready-made UIs in `res://addons/weavly/ui/`. They use only the engine's public API, so they work as they are, and they're also examples to copy and change.

## Setup

Instance a UI's scene and connect it to an engine, in one of two ways:

- **`engine`**: an engine node in the same scene.
- **`engine_autoload`**: the name of an autoloaded engine, looked up when the UI is ready.

Then start the dialogue on the engine, and the UI shows its lines and options as they come. The passage and card UIs work differently: they start nodes themselves, see below.

Each UI has its own `Theme`. To restyle one, change its theme, or copy its folder into your project and change the copy.

## Visual novel

`novel/weavly_novel_ui.tscn`, class `WeavlyNovelUI`: a textbox at the bottom of the screen with a nameplate, revealing each line letter by letter.

| Export | Default | Meaning |
|---|---|---|
| `characters_per_second` | `40` | how fast lines are revealed; `0` shows each line at once |
| `advance_action` | `ui_accept` | the input action that completes or continues a line, like a click |

## Passage

`passage/weavly_passage_ui.tscn`, class `WeavlyPassageUI`: a Twine-style page that shows a whole node at once, with its options as links.

```gdscript
$PassageUI.show_passage("Library")
```

`show_passage()` [renders](engine.md#rendering-a-whole-node) the node. Choosing a link renders what it leads to as the next passage.

| Export or signal | Meaning |
|---|---|
| `append` | keep earlier passages above the new one instead of replacing them |
| `finished` | emitted when a passage has no option left to choose |

## Cards

`card/weavly_card_ui.tscn`, class `WeavlyCardUI`: deals storylets from pools as cards. Each card is a [rendered](engine.md#rendering-a-whole-node) node, with its text and its options. Choosing an option on a card shows its outcome.

```gdscript
$CardUI.deal(["camp_actions"])
```

| Export or signal | Meaning |
|---|---|
| `hand_size` | the most cards a deal shows, `3` by default |
| `card_size`, `outcome_width` | the size of a card and the width of the outcome text |
| `hand_empty` | emitted when a deal finds no eligible storylet |


## Chat

`chat/weavly_chat_ui.tscn`, class `WeavlyChatUI`: a messenger, with typing indicators and the player's replies on the right.

| Export | Default | Meaning |
|---|---|---|
| `player_character` | empty | the character id whose lines are the player's own messages |
| `typing_speed` | `25` | characters per second the typing indicator waits for before another character's message |
| `min_wait`, `max_wait` | `0.6`, `3.0` | the shortest and longest typing wait, in seconds |
| `short_wait` | `0.4` | the pause before the player's own lines and narration |
| `advance_action` | `ui_accept` | shows a waiting message at once |
| `max_bubble_width`, `avatar_size` | `280`, `36×36` | message and avatar sizes |

## Speech bubbles

`bubble/weavly_bubble_ui.tscn`, class `WeavlyBubbleUI`: speech bubbles above the characters in your 2D or 3D scene.

Add a `WeavlySpeaker` node as a child of each character's `Node2D` or `Node3D`, and set its `character` to the character's id. Lines of that character show in a bubble pointing at it. Narration, lines of characters without a `WeavlySpeaker`, and options show in a bar at the bottom.

| Export | On | Meaning |
|---|---|---|
| `offset_2d`, `offset_3d` | `WeavlySpeaker` | where the bubble points, from the parent's position |
| `auto_advance` | `WeavlyBubbleUI` | seconds a line stays before the dialogue continues on its own, for barks; `0` waits for the player |
| `advance_action` | `WeavlyBubbleUI` | continues like a click on the bubble |
| `max_bubble_width`, `tail_size`, `screen_margin` | `WeavlyBubbleUI` | bubble sizes and the space kept from the screen's edges |

## Debug overlay

`debug/weavly_debug_ui.tscn`, class `WeavlyDebugUI`: an overlay for testing, with the dialogue's status, every variable, node and pool, and the runtime errors. Variables can be edited in place, and any node can be started from the list.

| Export | Default | Meaning |
|---|---|---|
| `toggle_action` | `weavly_toggle_debug` | shows and hides the overlay; bound to F3 if the project doesn't define it |
| `debug_builds_only` | `true` | leaves the overlay out of release builds |
| `refresh_interval` | `0.25` | seconds between refreshes while it shows |
| `max_errors` | `100` | how many errors it keeps |

## Characters

Two UIs read extra settings from [character resources](characters.md). Use these types instead of `WeavlyCharacter` for the characters that need them:

| Type | Adds | Used by |
|---|---|---|
| `WeavlyNovelCharacter` | `name_color`, the nameplate color | visual novel |
| `WeavlyChatCharacter` | `avatar` and `bubble_color` | chat |

## Choice lists

The UIs show options with `WeavlyChoiceList`, a `VBoxContainer` you can use in your own UI too. `show_options(options)` adds a button for each option, with locked ones disabled, and emits `chosen(option)` when the player picks one. Set `links` to show `LinkButton`s instead, and connect to `button_created(button, option)` to style each button as it's made.
