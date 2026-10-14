# Errors and warnings

## Errors

An error stops the build. It names the file, line and column:

```text
src/cave.wvl:2:1: error: unknown keyword '@jupm', did you mean '@jump'?
  2 | @jupm Ok
    | ^
```

Syntax errors show the line and point at the problem. Some add a hint:

```text
src/cave.wvl:4:1: error: unexpected '@endnode'
  4 | @endnode
    | ^
  hint: the @if block opened at line 2 must be closed with @endif first
```

Errors found after parsing, such as undeclared names or wrong types, are one line each, and the build reports all of them at once:

```text
src/shop.wvl:5:10: error: '+' needs a number, got a string
```

When the build fails, the previous `build/` folder stays as it was.

## Warnings

Warnings point at things that are probably mistakes but don't stop the build. They're printed after a successful build, in the same format:

```text
src/camp.wvl:2:5: warning: variable 'energy' is never used
```

The compiler warns about:

| Warning | Why it matters |
|---|---|
| a `var`, `extern var`, `character` or `func` that no file uses | it may be misspelled where it's used, or left over |
| a meta key that no node sets and nothing reads | it has no effect |
| a pool no node joins, and a slot with fewer than two nodes | a pool without nodes never offers anything, and a slot only matters between two nodes |
| `priority`, `weight` or `slot` on a node that's in no pool | they only matter when a pool is listed |
| a narration line with a `:` followed by a space within its first three words | it [looks like dialogue](../language/dialogue.md#narration-with-a-colon) |

For a narration line starting with `{name}:`, the warning suggests writing `name:` or `"{name}":` for dialogue.

## Silencing warnings

A comment `# weavly: ignore` at the end of a line silences every warning on that line:

```wvl
@env
var energy: number = 10  # weavly: ignore
@endenv
```

Spaces inside it are optional. An ignore comment that silences nothing is itself a warning, `weavly: ignore silences no warning`.

On narration and dialogue lines, `#` is text, so the comment doesn't work there. To silence the dialogue warning, write `\:` for the colon instead.

There's no way yet to make warnings fail the build, or to silence one kind of warning for the whole project.
