from infinitearithmetic import bigint, lang

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