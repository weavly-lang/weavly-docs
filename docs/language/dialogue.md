# Dialogue

A dialogue line is a speaker, a colon, a space and the text:

```wvl
@env
character Anna
character Ben
@endenv

@node Market
Anna: Have you seen Ben?
Ben: Right behind you.
@endnode
```

Spaces before the colon are allowed (`Anna : Hello.`). The space after it is required: `Anna:Hello` and `10:30` are narration.

The text works like [narration](text.md): it takes `{}` interpolation and the same escapes, and `#` is part of it.

## Speakers

A speaker is one of:

- **A declared character**, written as its name. Characters are declared in [`@env`](env.md#characters) with `character Anna`.
- **A `character` variable**, which speaks as whichever character it holds:

    ```wvl
    @env
    character Anna
    character Ben
    var companion: character = Anna
    @endenv

    @node Camp
    companion: Wait for me!
    @endnode
    ```

- **A quoted string**, for a one-off speaker that isn't worth declaring. It takes interpolation and escapes like any [quoted string](text.md#quoted-strings):

    ```wvl
    "Old Man": You shouldn't be here.
    "{Anna} and {Ben}": Surprise!
    ```

A name before the colon that isn't a character or a `character` variable is an error. If the name is close to a character's, the compiler suggests it, so `anna:` for a character `Anna` points you to `Anna`.

## Display names

A character's name in the script is its id. What the player sees is its display name, which the game owns and resolves each time a line runs. In the Godot addon, display names come from [character resources](../godot/characters.md).

Every place a character becomes text uses its display name: the speaker of a line, and `{Anna}` in a line or a string. This lets the game hide a name until the player learns it, for example by showing `???` at first.

A line with several speakers, like `"{Anna} and {Ben}"` above, is a one-off speaker with both display names in it.

## Narration with a colon

Whether a line is dialogue depends only on its shape: a name or quoted string, a colon and a space. A narration line that happens to have that shape needs `\:`:

```wvl
Day 3\: The village is quiet.
```

Without the escape, `Day` would be read as a speaker, and the build would fail because there's no character called `Day`.

The compiler also warns about narration lines that look like dialogue: a `:` followed by a space within the first three words. Write `\:` to keep the colon and silence the warning, or quote the speaker if it's meant to be dialogue.

## Portraits, emotions and voices

There's no special syntax for these. Call a [game function](env.md#functions) before the line:

```wvl
@do portrait(Anna, "angry")
Anna: You did what?
```
