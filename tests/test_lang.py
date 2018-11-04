from infinitearithmetic import bigint
from infinitearithmetic.lang import (Call, Token, eval_ast, eval_string,
                                     string_to_ast, lex, parse)


def test_eval_ast():
    # Parses basic calls
    assert(eval_ast(parse(lex('add(5, 10)'))) == bigint.fromint(15))
    assert(eval_ast(parse(lex('multiply(5, 10)'))) == bigint.fromint(50))

    # Parses nested calls
    assert(eval_ast(parse(lex('multiply(add(5, 10), 10)'))) == bigint.fromint(150))
    assert(eval_ast(parse(lex('multiply(5, add(multiply(2, 3), 10))')))
           == bigint.fromint(80))


def test_eval_string():
    # Ensure it's equivalent to making multiple calls
    assert(eval_string('add(5, 10)') == eval_ast(parse(lex('add(5, 10)'))))

    # Ensure nodesizes are adjusted
    assert(eval_string('add(5, 10)', 5) == bigint.fromint(15, 5))


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


def test_parse():
    # Parses basic expressions
    assert(parse(lex('4')) == bigint.fromint(4))
    assert(parse(lex('add(4, 1)')) == Call(
        'add', [bigint.fromint(4), bigint.fromint(1)]))
    assert(parse(lex('multiply(4, 1)')) == Call(
        'multiply', [bigint.fromint(4), bigint.fromint(1)]))

    # Parses nested expressions
    expected = Call('add', [Call(
        'multiply', [bigint.fromint(1), bigint.fromint(4)]), bigint.fromint(5)])
    assert(parse(lex('add(multiply(1, 4), 5)')) == expected)

    partial = Call('add', [bigint.fromint(1), bigint.fromint(4)])
    expected = Call('multiply', [partial, partial])
    assert(parse(lex('multiply(add(1, 4), add(1, 4))')) == expected)

    # Parses with nodesize
    assert(parse(lex('5'), 10) == bigint.fromint(5, 10))


def test_string_to_ast():
    # Ensure it's equivalent to making multiple calls
    assert(string_to_ast('add(1, 2)') == parse(lex('add(1, 2)')))

    # Ensure nodesizes are propagated
    assert(string_to_ast('add(1, 2)', 8) == parse(lex('add(1, 2)'), 8))
