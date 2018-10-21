from infinitearithmetic import lang

def test__string_to_ast__parses_add():
    ast = lang.string_to_ast('add(5, 10)')
    assert lang.eval_ast(ast) == 15

def test__string_to_ast__parses_multiply():
    ast = lang.string_to_ast('multiply(5, 10)')
    assert lang.eval_ast(ast) == 50

def test__string_to_ast__parses_compound_calls():
    ast = lang.string_to_ast('multiply(add(5, 10), 10)')
    assert lang.eval_ast(ast) == 150

    ast = lang.string_to_ast('multiply(5, add(multiply(2, 3), 10))')
    assert lang.eval_ast(ast) == 80