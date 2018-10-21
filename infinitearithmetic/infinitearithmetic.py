"""
Without recursion
"""

import sys

if __name__ == '__main__':
    import bigint
else:
    from . import bigint


def print_error(file, msg):
    print(file, 'infinitearithmetic: %s\n' % (msg))

def main():
    if len(sys.argv) < 2:
        print_error(sys.stderr, 'invalid arg count')
        sys.exit(1)

    try:
        assigns = [s.strip() for s in sys.argv[1].split(';')]
        args = dict([a.split('=') for a in assigns])
    except:
        print_error(sys.stderr, 'invalid args format')
        sys.exit(1)

    try:
        input_path = args['input']
    except KeyError:
        print_error(sys.stderr, '\'input\' is a required arg')
        sys.exit(1)

    try:
        digits = int(args['digitsPerNode'])
    except KeyError:
        print_error(sys.stderr, '\'digitsPerNode\' is a required arg')
        sys.exit(1)
    except TypeError:
        print_error(sys.stderr, '\'digitsPerNode\' is not an int')
        sys.exit(1)

    output = run_infinitearithmetic(input_path, digits)
    print(output)

    sys.exit(0)

def run_infinitearithmetic(input_path, digits_per_node):
    with open(input_path) as inputfile:
        exprs = [line.strip() for line in inputfile]
        exprs = [line for line in exprs if line]

    result_pairs = [(e, eval_expression(e, digits_per_node)) for e in exprs]
    formatted = [__format_eval_result(result, expr)
                 for expr, result in result_pairs]
    output = '\n'.join(formatted)

    return output


def eval_expression(expr, digits_per_node):
    try:
        expr = expr.strip()
        if '*' in expr:
            values = expr.split('*')
            x = bigint.parse(values[0], digits_per_node)
            y = bigint.parse(values[1], digits_per_node)
            return (True, bigint.multiply(x, y))

        elif '+' in expr:
            values = expr.split('+')
            x = bigint.parse(values[0], digits_per_node)
            y = bigint.parse(values[1], digits_per_node)
            return (True, bigint.add(x, y))
        else:
            return (False, ValueError('`expr` is an invalid expression'))
    except:
        return (False, ValueError('`expr` is an invalid expression'))


def __format_eval_result(result, expr):
    (successful, ret_val) = result
    if successful:
        return '%s=%s' % (expr, bigint.tostring(ret_val))
    else:
        return 'invalid expr `%s`' % (expr)
    


if __name__ == '__main__':
    main()
