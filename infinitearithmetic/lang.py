import re
from collections import namedtuple

from . import bigint
from lark import Lark, Transformer


Token = namedtuple('Token', ['text', 'lineno', 'offset'])


def eval_ast(ast):
    return AstTransformer().transform(ast)


class AstTransformer(Transformer):
    def expression(self, items):
        return items[0]

    def add(self, items):
        return bigint.add(items[0], items[1])

    def mul(self, items):
        return bigint.multiply(items[0], items[1])

    def number(self, items):
        return bigint.parse(items[0], 1)


def eval_string(string):
    return eval_ast(string_to_ast(string))


def lex(string):
    return _do_lex(string, None, 1, 0, [])


def _do_lex(string, filename, lineno, offset, acc):
    if not string:
        return acc
    stripped = string.strip()

    tok_offset = offset + (len(string) - len(stripped))

    matches = [r.match(stripped) for r in _token_regexes]
    matches = [m for m in matches if m]

    if not matches:
        raise SyntaxError('invalid syntax', (filename,
                                             lineno, tok_offset, stripped))

    if len(matches) > 1:
        raise SyntaxError('ambiguous syntax',
                          (filename, lineno, tok_offset, stripped))

    match = matches[0]
    new_str = match.re.sub('', stripped)
    new_str_offset = tok_offset + (len(stripped) - len(new_str))
    new_acc = acc + [Token(match.group(0), lineno, tok_offset)]

    return _do_lex(new_str, filename, lineno, new_str_offset, new_acc)


def _build_regex(pat):
    return re.compile('^(%s)' % pat)


_token_regexes = [
    _build_regex('\\('),
    _build_regex('\\)'),
    _build_regex(','),
    _build_regex('add'),
    _build_regex('multiply'),
    _build_regex('[\\d]+')
]


def string_to_ast(string):
    return __lark.parse(string)


__grammar = '''
expression: add
          | mul
          | number

add: "add" "(" expression "," expression ")"

mul: "multiply" "(" expression "," expression ")"

number: NUMBER

%import common.NUMBER
%import common.WS
%ignore WS
'''

__lark = Lark(__grammar, start='expression')
