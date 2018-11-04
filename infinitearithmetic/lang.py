"""Functions for evaluating the infinitearithmetic language.
"""

import re
from collections import namedtuple

from . import bigint


class Token(namedtuple('Token', ['text', 'lineno', 'offset'])):
    """Represents an important token in the parsing process."""


class Call(namedtuple('Call', ['name', 'args'])):
    """Represents a function call in an AST tree."""


def eval_ast(ast):
    """Evaluates an AST.

    Preconditions: 
        - `ast` is an AST, which is either a `Call` or a `BigInt`.
        - If `ast` is a `Call`, the call's `name` must be either `add` or `multiply`.

    Postconditions:
        - Returns a `BigInt`.
        - If any of the preconditions fail, raises a `ValueError`.
    """

    if isinstance(ast, Call):
        (name, args) = ast
        if name == 'add':
            return bigint.add(eval_ast(args[0]), eval_ast(args[1]))
        elif name == 'multiply':
            return bigint.multiply(eval_ast(args[0]), eval_ast(args[1]))
        else:
            raise ValueError('invalid call %s' % ast)
    elif isinstance(ast, bigint.BigInt):
        return ast
    else:
        raise ValueError('invalid ast \'%s\'' % ast)


def eval_string(string):
    """Evaluates a string.

    Preconditions:
        - `string` is a `str`.
        - `string` is in proper infinitearithmetic format.

    Postconditions:
        - Returns a `BigInt`.
        - If any of the preconditions fail, raises a `SyntaxError`.
    """

    return eval_ast(parse(lex(string)))


def lex(string):
    """Lexes a string into `Token`s.

    Preconditions:
        - `string` is a `str`.
        - `string` is in proper infinitearithmetic grammar.

    Postconditions:
        - Returns a list of `Token`s.
        - If `string` is not infinitearithmetic grammar, then a `SyntaxError`
          is raised.
    """

    return _do_lex(string, None, 1, 0, [])


# Internal usage
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


# Internal usage
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


def parse(tokens):
    """Evaluates a list of `Token`s into an ast.

    Preconditions:
        - `tokens` is a list of `Token`s.
        - `tokens` is in proper infinitearithmetic format.

    Postconditions:
        - Returns a `Call` or `BigInt`.
        - If `tokens` is not in proper infinitearithmetic format, raises a
          `SyntaxError`.
    """

    work_toks = list(tokens)
    result = _parse_expression(work_toks)

    if work_toks:
        tok = work_toks[0]
        raise SyntaxError('invalid syntax',
                          (None, tok.lineno, tok.offset, tok.text))

    return result


# Internal usage
def _consume_tok(tokens, text):
    tok = tokens[0]
    if not re.match('^%s' % text, tok.text):
        err_msg = 'expected \'%s\', got \'%s\'' % (text, tok.text)
        err_msg = err_msg.replace('\\', '')
        raise SyntaxError(err_msg, (None, tok.lineno, tok.offset, tok.text))

    tokens.pop(0)


# Internal usage
def _parse_integer(tokens):
    return bigint.fromstring(tokens.pop(0).text)


# Internal usage
def _parse_add(tokens):
    _consume_tok(tokens, 'add')
    _consume_tok(tokens, '\\(')

    a = _parse_expression(tokens)

    _consume_tok(tokens, ',')

    b = _parse_expression(tokens)

    _consume_tok(tokens, '\\)')

    return Call('add', [a, b])


# Internal usage
def _parse_mul(tokens):
    _consume_tok(tokens, 'multiply')
    _consume_tok(tokens, '\\(')

    a = _parse_expression(tokens)

    _consume_tok(tokens, ',')

    b = _parse_expression(tokens)

    _consume_tok(tokens, '\\)')

    return Call('multiply', [a, b])


# Internal usage
def _parse_expression(tokens):
    tok = tokens[0]
    if tok.text == 'add':
        return _parse_add(tokens)
    elif tok.text == 'multiply':
        return _parse_mul(tokens)
    elif re.match('[\\d]+', tok.text):
        return _parse_integer(tokens)
    else:
        raise SyntaxError('invalid syntax',
                          (None, tok.lineno, tok.offset, tok.text))


def string_to_ast(string):
    """Converts `string` to an ast.

    Preconditions:
        - `string` is a `str` of proper infinitearithmetic format.

    Postconditions:
        - Returns a `Call` or `BigInt`.
        - If any of the preconditions fail, a `SyntaxError` is raised.
    """
    return parse(lex(string))
