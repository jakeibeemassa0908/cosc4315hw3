"""A set of functions for working with bigints.
"""

from functools import reduce
from collections import namedtuple


class BigInt(namedtuple('BigInt', ['nodes', 'nodesize'])):
    """Data structure for holding arbitrarily large numbers.

    Because python already supports arbitrarily large numbers, there isn't
    a practical need for this type. However, the assignment is asking us to
    make this data structure for learning purposes.

    Attributes:
        nodes (List[int]): A list of symbolic digits for the data structure.
            Like any number system, the nodes represent one digit of the
            number. The maximum size of each node is determined by the BigInt's
            `nodesize`, which constrains the node's size to [0, 10^nodesize).

            The nodes are ordered from lowest value nodes to highest. For example,
            a number could be represented in the following form:

                155 #=> BigInt([5, 5, 1], 1)

        nodesize (int): The max size of each node, which constrains a node to
            the range [0, 10^nodesize].
    """


def add(bigint1, bigint2):
    """Sums two `BigInt`s.
    
    Preconditions:
        - `bigint1` and `bigint2` are a `BigInt`
        - `bigint1` and `bigint2` have the same nodesize.

    Postconditions:
        - Returns a `BigInt` contains the summed result.
        - If the nodesizes are different, raises a `ValueError`.
    """

    if bigint1.nodesize != bigint2.nodesize:
        raise ValueError('nodesizes do not match')

    new_len = max(len(bigint1.nodes), len(bigint2.nodes))
    new_nodesize = bigint1.nodesize

    nodes1 = bigint1.nodes + [0] * (new_len - len(bigint1.nodes))
    nodes2 = bigint2.nodes + [0] * (new_len - len(bigint2.nodes))

    added = [a + b for a, b in zip(nodes1, nodes2)]

    return BigInt(_nodes_norm(added, new_nodesize), new_nodesize)


def fromint(integer, nodesize=1):
    """Converts an `int` into a `BigInt`.
    
    Preconditions:
        - `integer` is an `int`.
        - `nodesize` is an `int`.

    Postconditions:
        - Returns a `BigInt`.
    """

    return fromstring(str(integer), nodesize)


def fromstring(string, nodesize=1):
    """Converts an `str` into a `BigInt`.
    
    Preconditions:
        - `string` is a `str` of digits.
        - `nodesize` is an `int`.

    Postconditions:
        - Returns a `BigInt`.
        - If `string` is not pure digits, raises a `ValueError`.
    """

    stripped = string.strip()
    if not stripped.isdigit():
        raise ValueError('string is not an integer')

    flipped = string[::-1]
    chunked = _chunkevery(flipped, nodesize)
    reverted = [n[::-1] for n in chunked]
    nodes = [int(n) for n in reverted]
    nodes = _nodes_norm(nodes, nodesize)
    return BigInt(nodes, nodesize)


def lshift(bigint, count):
    """Shifts the number's nodes `count` times to the left.
    
    This is effectively the equivalent of a bitshift left, but shifts by nodes
    instead of bits.
    
    Preconditions:
        - `bigint` is a `BigInt`.
        - `count` is an `int`.

    Postconditions:
        - Returns a `BigInt` shifted to the left `count` times.
    """

    new_nodes = ([0] * count) + bigint.nodes
    return BigInt(new_nodes, bigint.nodesize)


def multiply(bigint1, bigint2):
    """Multiplies two `BigInt`s.
    
    Preconditions:
        - `bigint1` and `bigint2` are a `BigInt`
        - `bigint1` and `bigint2` have the same nodesize.

    Postconditions:
        - Returns a `BigInt` contains the multiplied result.
        - If the nodesizes are different, raises a `ValueError`.
    """

    if bigint1.nodesize != bigint2.nodesize:
        raise ValueError('nodesizes do not match')

    nodes1 = bigint1.nodes
    nodes2 = bigint2.nodes
    new_nodesize = bigint1.nodesize

    # For each node n in bigint2, multiply it with each node m in bigint1
    multiplied = [[n1 * n2 for n1 in nodes1] for n2 in nodes2]
    # Create new bigints out of the new nodes.
    biginted = [BigInt(_nodes_norm(n, new_nodesize), new_nodesize)
                for n in multiplied]
    # Shift the new bigints based on their node position when multiplying
    shifted = [lshift(b, index) for index, b in enumerate(biginted)]
    return reduce(add, shifted)


def tostring(bigint):
    """Converts a `BigInt` to a `str`.
    
    Preconditions:
        - `bigint` is a `BigInt`.

    Postconditions:
        - Returns a `str` representation of `bigint`.
    """

    str_nodes = [str(n) for n in bigint.nodes]
    flipped_strs = str_nodes[::-1]
    padded = flipped_strs[:1] + \
        [s.zfill(bigint.nodesize) for s in flipped_strs[1:]]
    return ''.join(padded)


# Breaks iterables into lists of lists of size count.
def _chunkevery(iterable, count, acc=[]):
    if not iterable:
        return acc
    else:
        return _chunkevery(iterable[count:], count, acc + [iterable[:count]])


# Normalizes nodes to make sure each node is of appropriate size
def _nodes_norm(nodes, nodesize, carry=0, acc=[]):
    if not nodes:
        if carry > 0:
            return _nodes_norm([carry], nodesize, 0, acc)
        else:
            return _nodes_trim(acc)
    else:
        num, rest = nodes[0], nodes[1:]
        total = num + carry
        new_num = total % (10 ** nodesize)
        new_carry = total // (10 ** nodesize)
        return _nodes_norm(rest, nodesize, new_carry, acc + [new_num])


# Removes extra zeroes from nodes
def _nodes_trim(nodes):
    if not nodes:
        return [0]

    end, rest = nodes[-1], nodes[:-1]
    if end != 0:
        return nodes
    else:
        return _nodes_trim(rest)
