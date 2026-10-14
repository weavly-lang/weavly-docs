"""Pygments lexer for Weavly, a port of the Godot addon's WvlSyntaxHighlighter and WeavlyLineScanner."""

import re

from pygments.lexer import Lexer
from pygments.token import Comment, Keyword, Name, Number, String, Text

TEXT = Text
DIRECTIVE = Keyword.Reserved
VARIABLE = Name.Variable
STRING = String
NUMBER = Number
CHARACTER = Name.Entity
COMMENT = Comment
KEYWORD = Keyword
FUNCTION = Name.Function
META = Name.Attribute
NODE = Name.Label

KIND_TOKENS = {
    "node": NODE,
    "pool": NODE,
    "slot": NODE,
    "character": CHARACTER,
    "var": VARIABLE,
    "meta": META,
    "func": FUNCTION,
}

# Names known for the page being rendered, set by the MkDocs hook: name -> kind.
NAMES: dict[str, str] = {}

NONE, ENV, BODY, META_BLOCK = range(4)
P_TEXT, P_CODE, P_STRING, P_COMMENT, P_SPEAKER = range(5)

_A = re.ASCII
_DIRECTIVE_START = re.compile(r"^[ \t]*(@[A-Za-z_]\w*)", _A)
_SPEAKER = re.compile(r'(?:[A-Za-z_]\w*|"(?:\\.|[^"\\])*")[ \t]*:(?=[ \t])', _A)

_NUMBER = re.compile(r"\b\d+(?:\.\d+)?\b", _A)
_NAME = re.compile(r"(?<![@.\w])[A-Za-z_]\w*(?![\w(])", _A)
_DIRECTIVE = re.compile(r"@[A-Za-z_]+", _A)
_KEYWORD = re.compile(r"(?<![@\w])(?:and|or|not|true|false|var)(?!\w)", _A)
_FUNCTION = re.compile(r"(?<![@\w])[A-Za-z_]\w*(?=\()", _A)
_META_READ = re.compile(r"\.[A-Za-z_]\w*", _A)
_KIND = re.compile(r"^[ \t]*((?:extern[ \t]+)?var|pool|slot|character|meta|func)(?!\w)", _A)
_TYPE = re.compile(r":[ \t]*(?:var[ \t]+)?(number|string|bool|node|pool|slot|character)(?!\w)", _A)
_VAR_PARAM = re.compile(r":[ \t]*(var)[ \t]", _A)
_BOOL_VALUE = re.compile(r"=[ \t]*(true|false)(?!\w)", _A)
_META_KEY = re.compile(r"^[ \t]*([A-Za-z_]\w*)[ \t]*:", _A)
_OPTION_CALL = re.compile(r"^[ \t]*@option[ \t]+(node|pool)\(", _A)
_POOL_PARAMETER = re.compile(r"(?<!\w)(limit|shuffle|locked)(?=[ \t]*:)", _A)
_LOCKED_VALUE = re.compile(r"locked[ \t]*:[ \t]*(show|extra|hide)(?!\w)", _A)

_DECLARATION = re.compile(r"^\s*(?:extern\s+)?(var|pool|slot|character|meta|func)\s+([A-Za-z_]\w*)", _A)
_NODE_LINE = re.compile(r"^[ \t]*@node[ \t]+([A-Za-z_]\w*)", _A)

# Docs-only: kinds read from where an undeclared name is used, since examples are fragments.
_USES = [
    (re.compile(r"@(?:jump|detour)[ \t]+([A-Za-z_]\w*)", _A), "node"),
    (re.compile(r"@(?:set|increase|decrease)[ \t]+([A-Za-z_]\w*)", _A), "var"),
    (re.compile(r"\b(?:visited|visit_count|skip_count|node)\([ \t]*([A-Za-z_]\w*)", _A), "node"),
    (re.compile(r"(?<![.\w])([A-Za-z_]\w*)\.[A-Za-z_]", _A), "node"),
    (re.compile(r"^[ \t]*([A-Za-z_]\w*)[ \t]*:[ \t]", _A), "character"),
    (re.compile(r"\{([A-Z]\w*)\}", _A), "character"),
]
_LIST_USES = [
    (re.compile(r"@draw[ \t]+([^#\n]+)", _A), "pool"),
    (re.compile(r"@option[ \t]+pool\(([^)]*)\)", _A), "pool"),
]
_GROUP_ENTRY = re.compile(r"^\s*(pool|slot)\s*:([^#]*)", _A)
_ID = re.compile(r"^[A-Za-z_]\w*$", _A)
_WORDS = frozenset(
    "and or not true false var extern first last all show extra hide limit shuffle locked "
    "number string bool node pool slot character meta func".split()
)


def next_block(block: int, text: str) -> int:
    found = directive(text)
    if block == ENV:
        return NONE if found == "@endenv" else block
    if block == META_BLOCK:
        return BODY if found == "@endmeta" else block
    return {
        "@env": ENV,
        "@node": BODY,
        "@endnode": NONE,
        "@meta": META_BLOCK if block == BODY else block,
    }.get(found, block)


def directive(text: str) -> str:
    found = _DIRECTIVE_START.search(text)
    return "" if found is None else found.group(1)


def blocks(lines: list[str]) -> list[int]:
    result = []
    block = NONE
    for line in lines:
        result.append(block)
        block = next_block(block, line)
    return result


def parts(text: str, block: int) -> list[int]:
    result = [P_TEXT] * len(text)
    if block in (ENV, META_BLOCK):
        _scan_code(text, 0, result, False)
    else:
        _scan_line(text, 0, result)
    return result


def _scan_line(text: str, start: int, result: list[int]) -> None:
    i = start
    while i < len(text) and text[i] in " \t":
        i += 1
    if i >= len(text):
        return
    if text[i] == "#":
        _mark(result, i, len(text), P_COMMENT)
    elif text[i] == "@":
        colon = _scan_code(text, i, result, True)
        if colon >= 0:
            _scan_line(text, colon + 1, result)
    else:
        speaker = _SPEAKER.match(text, i)
        if speaker is not None:
            _scan_speaker(text, i, speaker.end(), result)
            i = speaker.end()
        _scan_text(text, i, result)


def _scan_speaker(text: str, start: int, end: int, result: list[int]) -> None:
    if text[start] == '"':
        _scan_string(text, start, result)
    for i in range(start, end):
        if result[i] != P_CODE:
            result[i] = P_SPEAKER


def _scan_code(text: str, start: int, result: list[int], stop_at_colon: bool) -> int:
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == '"':
            i = _scan_string(text, i, result)
            continue
        if c == "#":
            _mark(result, i, len(text), P_COMMENT)
            return -1
        if c == ":" and depth == 0 and stop_at_colon:
            return i
        if c in "([":
            depth += 1
        elif c in ")]":
            depth = max(depth - 1, 0)
        result[i] = P_CODE
        i += 1
    return -1


def _scan_string(text: str, start: int, result: list[int]) -> int:
    result[start] = P_STRING
    i = start + 1
    while i < len(text) and text[i] != '"':
        if text[i] == "\\":
            _mark(result, i, i + 2, P_STRING)
            i += 2
        elif text[i] == "{":
            i = _scan_interpolation(text, i, result)
        else:
            result[i] = P_STRING
            i += 1
    _mark(result, i, i + 1, P_STRING)
    return i + 1


def _scan_text(text: str, start: int, result: list[int]) -> None:
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
        elif text[i] == "{":
            i = _scan_interpolation(text, i, result)
        else:
            i += 1


def _scan_interpolation(text: str, start: int, result: list[int]) -> int:
    i = start + 1
    quoted = False
    while i < len(text) and (quoted or text[i] != "}"):
        if text[i] == '"':
            quoted = not quoted
            result[i] = P_STRING
        else:
            result[i] = P_STRING if quoted else P_CODE
        i += 1
    return i + 1


def _mark(result: list[int], start: int, end: int, part: int) -> None:
    for i in range(start, min(end, len(result))):
        result[i] = part


def highlight_line(text: str, block: int, names: dict[str, str]) -> list:
    colors = [TEXT] * len(text)
    _paint_numbers(colors, text)
    _paint_names(colors, text, block, names)
    if block == ENV:
        for regex in (_KIND, _TYPE, _VAR_PARAM, _BOOL_VALUE):
            _paint(colors, text, regex, KEYWORD, 1)
    elif block == META_BLOCK:
        _paint(colors, text, _META_KEY, META, 1)
        _paint_expression_words(colors, text)
    else:
        _paint_expression_words(colors, text)
        if _OPTION_CALL.search(text):
            _paint(colors, text, _POOL_PARAMETER, KEYWORD, 1)
            _paint(colors, text, _LOCKED_VALUE, KEYWORD, 1)
    _paint(colors, text, _DIRECTIVE, DIRECTIVE)
    for i, part in enumerate(parts(text, block)):
        if part == P_TEXT:
            colors[i] = TEXT
        elif part == P_STRING:
            colors[i] = STRING
        elif part == P_COMMENT:
            colors[i] = COMMENT
        elif part == P_SPEAKER:
            colors[i] = CHARACTER
    return colors


def _paint(colors: list, text: str, regex: re.Pattern, token, group: int = 0) -> None:
    for match in regex.finditer(text):
        for i in range(match.start(group), match.end(group)):
            colors[i] = token


# Docs-only fallback for undeclared names, after the naming convention: PascalCase is a node.
def _guess(name: str) -> str | None:
    if name in _WORDS:
        return None
    return "node" if name[0].isupper() else "var"


def _paint_names(colors: list, text: str, block: int, names: dict[str, str]) -> None:
    for match in _NAME.finditer(text):
        kind = names.get(match.group())
        if kind is None and (block != ENV or match.group()[0].isupper()):
            kind = _guess(match.group())
        if kind is None:
            continue
        for i in range(match.start(), match.end()):
            colors[i] = KIND_TOKENS[kind]


def _paint_expression_words(colors: list, text: str) -> None:
    _paint(colors, text, _KEYWORD, KEYWORD)
    _paint(colors, text, _FUNCTION, FUNCTION)
    _paint(colors, text, _META_READ, META)


def _paint_numbers(colors: list, text: str) -> None:
    for match in _NUMBER.finditer(text):
        start = match.start()
        if start > 0 and text[start - 1] == "-" and _starts_negative_number(text, start - 1):
            start -= 1
        for i in range(start, match.end()):
            colors[i] = NUMBER


def _starts_negative_number(text: str, minus: int) -> bool:
    for i in range(minus - 1, -1, -1):
        if text[i] in " \t":
            continue
        return text[i] in "=(,[+-*/<>!"
    return True


def collect_names(sources: list[str]) -> dict[str, str]:
    """Kinds of the names declared in the sources, then of undeclared names by where they're used."""
    declared: dict[str, str] = {}
    used: dict[str, str] = {}
    for source in sources:
        lines = source.splitlines()
        for line, block in zip(lines, blocks(lines)):
            node = _NODE_LINE.search(line)
            if node:
                declared.setdefault(node.group(1), "node")
            if block == ENV:
                declaration = _DECLARATION.search(line)
                if declaration:
                    declared.setdefault(declaration.group(2), declaration.group(1))
                continue
            if block == META_BLOCK:
                entry = _GROUP_ENTRY.search(line)
                if entry:
                    for name in entry.group(2).split(","):
                        if _ID.match(name.strip()):
                            used.setdefault(name.strip(), entry.group(1))
                continue
            for regex, kind in _USES:
                for match in regex.finditer(line):
                    if match.group(1) not in _WORDS:
                        used.setdefault(match.group(1), kind)
            for regex, kind in _LIST_USES:
                for match in regex.finditer(line):
                    for argument in match.group(1).split(","):
                        name = argument.strip()
                        if _ID.match(name) and name not in _WORDS:
                            used.setdefault(name, kind)
    return {**used, **declared}


class WvlLexer(Lexer):
    name = "Weavly"
    aliases = ["wvl", "weavly"]
    filenames = ["*.wvl"]

    def get_tokens_unprocessed(self, text):
        names = {**NAMES, **collect_names([text])}
        lines = text.split("\n")
        offset = 0
        for index, (line, block) in enumerate(zip(lines, blocks(lines))):
            colors = highlight_line(line, block, names)
            start = 0
            for i in range(1, len(line) + 1):
                if i == len(line) or colors[i] != colors[start]:
                    yield offset + start, colors[start], line[start:i]
                    start = i
            offset += len(line)
            if index < len(lines) - 1:
                yield offset, Text, "\n"
                offset += 1
