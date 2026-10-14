# Expressions

Expressions appear in conditions, `@set`, `{}` in text, function arguments, weights and `@meta` values.

## Values

| Write | Type |
|---|---|
| `3`, `-2.5`, `.5` | `number` |
| `"text"`, `"Hi {name}"` | `string`, see [Quoted strings](text.md#quoted-strings) |
| `true`, `false` | `bool` |
| `gold` | the value of the variable `gold` |
| `Cave` | the node `Cave` itself |

A name always means its value. For a variable that's what it holds. For a node, pool, slot or character, it's that node, pool, slot or character, so `@set next_room = Cave` stores the node.

## Operators

From lowest to highest precedence:

| Operator | Meaning | Operands |
|---|---|---|
| `or` | either is true | bools |
| `and` | both are true | bools |
| `not` | the opposite | a bool |
| `==`, `!=` | equal, not equal | two values of the same type |
| `<`, `>`, `<=`, `>=` | comparisons | numbers |
| `+`, `-` | add, subtract | numbers |
| `*`, `/` | multiply, divide | numbers |
| `-` | negate | a number |

Use parentheses to group: `(gold + bonus) * 2`.

Comparisons don't chain: `1 < x < 5` is an error. Write `1 < x and x < 5`.

`+` only adds numbers. To join strings, use interpolation: `"{first} {last}"`.

## Types

Every expression has a type, checked when the project is built:

- `number`, `string` and `bool` for values.
- `node`, `pool`, `slot` and `character` for names, and for variables that hold them.

Each place takes a type:

- Conditions (`@if`, `@elif`, `@when`, option and case conditions, and the `when` and `available` meta keys) need a bool.
- `@set` needs the variable's type. `@increase` and `@decrease` need a number variable and a number amount.
- Weights, `priority` and `weight` need numbers.
- `{}` in text takes any type.

## Built-in functions

| Function | Returns |
|---|---|
| `random(a, b)` | a random whole number from `a` to `b`, both included |
| `min(a, b, ...)`, `max(a, b, ...)` | the smallest or largest of two or more numbers |
| `clamp(x, low, high)` | `x` kept between `low` and `high` |
| `round(x)`, `floor(x)`, `ceil(x)` | `x` rounded to the nearest, next lower or next higher whole number |
| `abs(x)` | `x` without its sign |

## Node functions

| Function | Returns |
|---|---|
| `visited(node)` | whether the node has been visited, a bool |
| `visit_count(node)` | how often the node has been visited |
| `skip_count(node)` | how often the node could have been taken from a pool but wasn't, see [Storylets](meta.md#skip-count) |

Without an argument, they mean the node they're written in:

```
@node Shrine
@if visited(): The shrine is as quiet as last time.
@if visit_count(Tavern) > 3: You smell of ale.
@endnode
```

A node counts as visited [when it ends](statements.md#visits). The argument is a node name or a `node` variable.

## Meta values

`.key` reads a [meta value](meta.md#reading-meta-values) of the current node, and `Node.key` one of another node. Write them without spaces: `.cost`, `Smithy.cost`, `next_room.cost`.

## Game functions

Functions the game provides are called like built-in ones, once they're [declared](env.md#functions) with a return type:

```
@if trust(Anna, Ben) > 5: Anna: I'd trust him with my life.
```
