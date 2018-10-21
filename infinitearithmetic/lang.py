from lark import Lark, Transformer


def eval_ast(ast):
    return AstTransformer().transform(ast)


class AstTransformer(Transformer):
    def expression(self, items):
        return items[0]

    def add(self, items):
        return items[0] + items[1]

    def mul(self, items):
        return items[0] * items[1]

    def number(self, items):
        return int(items[0])


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
