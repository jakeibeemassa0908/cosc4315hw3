"""A set of functions for working with bigints.
"""

from functools import reduce
from collections import namedtuple

def add(bigint1, bigint2):
    nodes1 = bigint1[2]
    nodes2 = bigint2[2]
    new_nodesize = bigint1[1]

    nodes1 = nodes1 + [0] * (len(nodes2) - len(nodes1))
    nodes2 = nodes2 + [0] * (len(nodes1) - len(nodes2))

    added = [a + b for a, b in zip(nodes1, nodes2)]
    normalized = __nodes_normalize(added, new_nodesize)

    return new(new_nodesize, normalized)


def __nodes_normalize(nodes, nodesize, carry=0, acc=[]):
    if not nodes:
        if carry > 0:
            return __nodes_normalize([carry], nodesize, 0, acc)
        else:
            return __nodes_strip_zeroes(acc)
    else:
        num, rest = nodes[0], nodes[1:]
        total = num + carry
        new_num = total % (10 ** nodesize)
        new_carry = total // (10 ** nodesize)
        return __nodes_normalize(rest, nodesize, new_carry, acc + [new_num])


def __nodes_strip_zeroes(nodes):
    if not nodes:
        return [0]

    end, rest = nodes[-1], nodes[:-1]
    if end != 0:
        return nodes
    else:
        return __nodes_strip_zeroes(rest)


def fromint(integer, nodesize=1):
    return parse(str(integer), nodesize)


def isbigint(value):
    return isinstance(value, tuple) and len(value) == 3 and value[0] == 'bigint'


def multiply(bigint1, bigint2):
    nodes1 = bigint1[2]
    nodes2 = bigint2[2]
    new_nodesize = bigint1[1]

    # For each node n in bigint2, multiply it with each node m in bigint1
    multiplied = [[n1 * n2 for n1 in nodes1] for n2 in nodes2]
    # Create new bigints out of the new nodes.
    biginted = [new(new_nodesize, n) for n in multiplied]
    # Shift the new bigints based on their node position when multiplying
    shifted = [lnodeshift(b, index) for index, b in enumerate(biginted)]
    return reduce(add, shifted)


def new(nodesize, nodes):
    nodes = __nodes_normalize(nodes, nodesize)
    return ('bigint', nodesize, nodes)


def parse(string, nodesize=1):
    string = string.strip()
    if not string.isdigit():
        raise ValueError('`string is not a parseable bigint.')

    flipped = string[::-1]
    chunked = __chunkevery(flipped, nodesize)
    reverted = [n[::-1] for n in chunked]
    nodes = [int(n) for n in reverted]
    nodes = __nodes_normalize(nodes, nodesize)
    return new(nodesize, nodes)


def lnodeshift(bigint, count):
    return new(bigint[1], ([0] * count) + bigint[2])


def __chunkevery(iterable, count, acc=[]):
    if not iterable:
        return acc
    else:
        return __chunkevery(iterable[count:], count, acc + [iterable[:count]])


def tostring(bigint):
    nodes = bigint[2]
    if not nodes:
        return '0'
    else:
        nodesize = bigint[1]
        stringified = [str(n) for n in nodes]
        padded = [n.zfill(nodesize)
                  for n in stringified[:-1]] + stringified[-1:]
        return ''.join(reversed(padded))
