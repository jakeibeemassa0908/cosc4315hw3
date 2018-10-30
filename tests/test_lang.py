from infinitearithmetic import bigint, lang
from infinitearithmetic.lang import lex, Token


def test__string_to_ast__parses_add():
    ast = lang.string_to_ast('add(5, 10)')
    assert lang.eval_ast(ast) == bigint.fromint(15, 1)


def test__string_to_ast__parses_multiply():
    ast = lang.string_to_ast('multiply(5, 10)')
    assert lang.eval_ast(ast) == bigint.fromint(50, 1)


def test__string_to_ast__parses_compound_calls():
    ast = lang.string_to_ast('multiply(add(5, 10), 10)')
    assert lang.eval_ast(ast) == bigint.fromint(150, 1)

    ast = lang.string_to_ast('multiply(5, add(multiply(2, 3), 10))')
    assert lang.eval_ast(ast) == bigint.fromint(80, 1)


def test_lex():
    # Recognizes standard tokens
    assert(lex('add') == [Token('add', 1, 0)])
    assert(lex('multiply') == [Token('multiply', 1, 0)])
    assert(lex('()') == [Token('(', 1, 0), Token(')', 1, 1)])
    assert(lex(',') == [Token(',', 1, 0)])

    # Can lex complex expression
    add_toks = [
        Token('add', 1, 0),
        Token('(', 1, 3),
        Token('4', 1, 4),
        Token(',', 1, 5),
        Token('1', 1, 6),
        Token(')', 1, 7)
    ]
    assert(lex('add(4,1)') == add_toks)

    # Tracks whitespace
    assert(lex('   (') == [Token('(', 1,  3)])
