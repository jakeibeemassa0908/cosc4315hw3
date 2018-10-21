from . import bigint
from lark import Lark, Transformer


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
