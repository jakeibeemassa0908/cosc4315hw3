"""
Without recursion
"""

import sys

from . import bigint
from .lang import eval_string


def main():
    if len(sys.argv) < 2:
        _print_error(sys.stderr, 'invalid arg count')
        sys.exit(1)

    try:
        assigns = [s.strip() for s in sys.argv[1].split(';')]
        args = dict([a.split('=') for a in assigns])
    except:
        _print_error(sys.stderr, 'invalid args format')
        sys.exit(1)

    try:
        input_path = args['input']
    except KeyError:
        _print_error(sys.stderr, '\'input\' is a required arg')
        sys.exit(1)

    try:
        digits = int(args['digitsPerNode'])
    except KeyError:
        _print_error(sys.stderr, '\'digitsPerNode\' is a required arg')
        sys.exit(1)
    except TypeError:
        _print_error(sys.stderr, '\'digitsPerNode\' is not an int')
        sys.exit(1)

    with open(input_path) as inputfile:
        stripped = (l.strip() for l in inputfile)
        exprs = (l for l in stripped if l)

    equations = [(e, _safe_call(eval_string, e)) for e in exprs]
    str_results = [_fmt_result(e[0], e[1]) for e in equations]
    output = '\n'.join(str_results)

    print(output)

    sys.exit(0)


def _fmt_result(result, expr):
    success, val = result
    if success:
        return '%s = %s' % (expr, bigint.tostring(val))
    else:
        return '%s = invalid expression' % (expr)


def _print_error(file, msg):
    print('infinitearithmetic: %s' % (msg), file=file)


def _safe_call(fun, *args):
    try:
        return (True, fun(*args))
    except BaseException as e:
        return (False, e)


if __name__ == '__main__':
    main()
