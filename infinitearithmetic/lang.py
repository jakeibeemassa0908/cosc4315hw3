import re
from collections import namedtuple

from . import bigint

Token = namedtuple('Token', ['text', 'lineno', 'offset'])

Call = namedtuple('Call', ['name', 'args'])


def eval_ast(ast):
    if isinstance(ast, Call):
        (name, args) = ast
        if name == 'add':
            return eval_ast(args[0]) + eval_ast(args[1])
        elif name == 'multiply':
            return eval_ast(args[0]) * eval_ast(args[1])
        else:
            raise ValueError('invalid call %s' % ast)
    elif isinstance(ast, int):
        return ast
    else:
        raise ValueError('invalid ast \'%s\'' % ast)


def eval_string(string):
    return eval_ast(parse(lex(string)))


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


def parse(tokens):
    work_toks = list(tokens)
    result = _parse_expression(work_toks)

    if work_toks:
        tok = work_toks[0]
        raise SyntaxError('invalid syntax',
                          (None, tok.lineno, tok.offset, tok.text))

    return result


def _consume_tok(tokens, text):
    tok = tokens[0]
    if not re.match('^%s' % text, tok.text):
        err_msg = 'expected \'%s\', got \'%s\'' % (text, tok.text)
        err_msg = err_msg.replace('\\', '')
        raise SyntaxError(err_msg, (None, tok.lineno, tok.offset, tok.text))

    tokens.pop(0)


def _parse_integer(tokens):
    return int(tokens.pop(0).text)


def _parse_add(tokens):
    _consume_tok(tokens, 'add')
    _consume_tok(tokens, '\\(')

    a = _parse_expression(tokens)

    _consume_tok(tokens, ',')

    b = _parse_expression(tokens)

    _consume_tok(tokens, '\\)')

    return Call('add', [a, b])


def _parse_mul(tokens):
    _consume_tok(tokens, 'multiply')
    _consume_tok(tokens, '\\(')

    a = _parse_expression(tokens)

    _consume_tok(tokens, ',')

    b = _parse_expression(tokens)

    _consume_tok(tokens, '\\)')

    return Call('multiply', [a, b])


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
