# Text

## Narration

Any line inside a node that isn't a keyword, a comment or [dialogue](dialogue.md) is narration:

```
@node Tavern
The tavern is warm and loud.
Someone is playing a fiddle in the corner.
@endnode
```

Each narration line is shown on its own and pauses until the player continues. Spaces at the start and end of the line are dropped.

## Interpolation

Text can hold [expressions](expressions.md) in `{}`. They're evaluated when the line is shown, and the result is put into the text:

```
You have {gold} gold.
The room costs {base_price * markup} gold.
```

Values are written like this:

| Value | Shown as |
|---|---|
| Whole number | without decimals: `3`, not `3.0` |
| Other number | rounded to two decimals: `2.5`, `0.33` |
| `true`, `false` | `true`, `false` |
| Node, pool or slot | its name |
| Character | its display name, see [Dialogue](dialogue.md#display-names) |

A value is put into the text once, when the line runs. Changing the variable later doesn't change a line that was already shown.

## Escapes in text

| Write | To get |
|---|---|
| `\{` | a literal `{` |
| `\:` | a literal `:` that never makes the line dialogue, see [Dialogue](dialogue.md#narration-with-a-colon) |

A `}` outside an expression is plain text and needs no escape. Any other backslash is kept as written.

## Hash signs

On narration and dialogue lines, `#` is text, not a comment:

```
Prices start at #5.
```

Comments work at the end of every other line and on lines of their own.

## Quoted strings

Strings in `"..."` appear in expressions, option labels, [`@continue`](options.md#continue), one-off speakers and `@meta` values:

```
@set title = "Captain"
@option "Ask about the ship": @detour Ship
```

A quoted string is kept exactly as written, spaces included. It takes the same `{}` interpolation as a line:

```
@set greeting = "Hello, {player_name}!"
```

Quoted strings support these escapes:

| Write | To get |
|---|---|
| `\"` | a quote |
| `\\` | a backslash |
| `\n`, `\t` | a line break, a tab |
| `\uXXXX` | the Unicode character with that hex code |
| `\{` | a literal `{` |

A string inside `{}` in a quoted string escapes its quotes like any other quote: `"Greet {name == \"Bob\"}"`.

## When interpolation runs

`{}` is evaluated when the expression around it is:

- in a line, when the line is shown
- in `@set`, when the `@set` runs, so the variable keeps the text as it was at that moment
- in a function argument, when the function is called
- in a condition, each time the condition is checked
- in a `@meta` value, each time the value is read

Defaults in [`@env`](env.md) are constants, so they can't hold `{}`. Write `\{` for a literal brace there.
