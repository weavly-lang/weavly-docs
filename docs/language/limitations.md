# Limitations

Weavly is in alpha. These are things the language doesn't do yet, and how to work around them where possible.

## Flow

- **No `@return`.** A [detour](statements.md#detour) returns when its node runs out of statements. Use `@if` to skip the rest of a node.
- **`@draw` can't tell whether it drew anything.** Give the pool a [fallback node](meta.md#how-nodes-are-picked), or have the drawn nodes set a variable.
- **`@draw` has no parameters** such as `limit` or `shuffle`. A [`pool(...)` option](options.md#pool) has them.
- **Targets are names or variables only.** `@jump`, `@detour`, `@draw` and node functions don't take function results or other expressions. Store the target in a `node` or `pool` variable first.

## Functions

- **No optional or variadic parameters.** Every call passes exactly the declared parameters.

## Meta

- **Custom meta keys have no ranges and no list values.**
- **No meta on inline options.** Write the option as its own node and offer it with [`node(...)`](options.md#node).

## Warnings

- **No `--strict`** to make warnings fail the build, and no way to silence one kind of warning for the whole project. `# weavly: ignore` silences the warnings on one line.

## Localization

There's no built-in localization yet.
