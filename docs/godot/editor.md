# Editor

The addon adds a **Weavly** screen to the Godot editor, next to 2D, 3D and Script, for writing and compiling `.wvl` files.

## Opening and creating files

Double-click a `.wvl` file in the FileSystem dock to open it. To create one, right-click a folder and choose *Create New → WeavlyFile...*.

The editor remembers the open file between sessions.

## Compiling

Click **Compile** in the toolbar, or turn on **Compile on save**. The editor saves the file and builds the project it belongs to: the folder above the nearest `src` folder, so `res://dialogue/src/cave.wvl` builds `res://dialogue`.

The status in the toolbar shows the result, and the Output panel has the compiler's messages. When the build fails, the caret jumps to the first error in the open file.

The editor needs compiler 0.7. It warns in the Output panel when it finds another version or no compiler.

## Writing

- **Syntax highlighting**, with names colored by what they're declared as anywhere in the project.
- **Go to node**: a list of the file's nodes in the toolbar, to jump to one. In the text, a line separates the nodes and each `@node` line has a tinted background.
- **Hover** over a name to see its declaration and how often it's used. For a pool or slot, the tooltip lists its nodes.
- **Ctrl+click** a name to go to its declaration. On a declaration, Ctrl+click lists every use.

| Shortcut | Does |
|---|---|
| Ctrl+S | save |
| Ctrl+F | find |
| Ctrl+H | find and replace |
| F3, Shift+F3 | next and previous match |
| Alt+Left, Alt+Right | back and forward after jumping, also the mouse's back and forward buttons |

## Settings

Under *Editor → Editor Settings → Weavly*:

| Setting | Default | Meaning |
|---|---|---|
| `executable_path` | `weavly` | the compiler to run, if it isn't on your `PATH` as `weavly` |
| `compile_on_save` | off | build after every save, also the toolbar toggle |
| `line_wrap` | on | wrap long lines, also the toolbar toggle |
| `node_separator` | on | the line between nodes |
| `node_tint` | on | the tinted background of each `@node` line |
