# API reference

The classes a game uses. The guides on the other pages show how they work together. Detailed documentation of every member is coming to Godot's built-in help, so you'll find it with *Search Help* (F1) in the editor, matching the addon version you have installed.

## Engine

| Class | What it is |
|---|---|
| `WeavlyEngine` | the node that runs dialogue, see [Running dialogue](engine.md) |
| `WeavlyEngine.Locked` | how pools count locked nodes, see [Listing a pool](storylets.md#listing-a-pool) |

## What the engine passes

| Class | What it is |
|---|---|
| `WeavlyModel.LineStatement` | a line, either `NarrationLine` or `CharacterLine`, see [Lines](engine.md#lines) |
| `WeavlyModel.Option` | an offered option, see [Options](engine.md#options) |
| `WeavlyModel.OptionBlock` | a rendered option block, with its `options` |
| `WeavlyModel.DoStatement` | a rendered `@do`, with its `id` and evaluated `values` |
| `WeavlyModel.Statement` | the base of every statement, with its `source` and `line` |

## Characters

| Class | What it is |
|---|---|
| `WeavlyCharacter` | a character's display name, see [Characters](characters.md) |
| `WeavlyNovelCharacter`, `WeavlyChatCharacter` | characters with extra settings for the [starter UIs](ui.md#characters) |

## Services

| Class | What it is |
|---|---|
| `WeavlyService` | the base of every service, see [Custom services](services.md) |
| `WeavlyCharacterService`, `WeavlyCountService`, `WeavlyFunctionService`, `WeavlyLineService`, `WeavlyVariableService` | the services to replace |
| `WeavlyDefault*Service` | the default implementations, to extend |

## Starter UIs

| Class | What it is |
|---|---|
| `WeavlyUI` | the base of every starter UI, with `engine` and `engine_autoload` |
| `WeavlyNovelUI`, `WeavlyPassageUI`, `WeavlyCardUI`, `WeavlyChatUI`, `WeavlyBubbleUI`, `WeavlyDebugUI` | the [starter UIs](ui.md) |
| `WeavlySpeaker` | marks a node as a character for the speech bubbles |
| `WeavlyChoiceList` | a list of option buttons, see [Choice lists](ui.md#choice-lists) |
