"""
Without recursion
"""

import sys

from . import bigint, lang


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

    with open(input_path) as inputfile:
        stripped = (l.strip() for l in inputfile)
        exprs = (l for l in stripped if l)

    results = (__safe_eval_string(e, digits) for e in exprs)
    formatted = (__format_eval_result(pair[0], pair[1])
                 for pair in zip(exprs, results))
    output = '\n'.join(formatted)

    print(output)

    sys.exit(0)


def __safe_eval_string(string, digits):
    try:
        return (True, lang.eval_string(string))
    except:
        return (False, ValueError('Something weird'))


def __format_eval_result(result, expr):
    (successful, ret_val) = result
    if successful:
        return '%s=%s' % (expr, bigint.tostring(ret_val))
    else:
        return 'invalid expr `%s`' % (expr)


if __name__ == '__main__':
    main()
