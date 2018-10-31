"""A set of functions for working with bigints.
"""

from collections import namedtuple


class BigInt(namedtuple('BigInt', ['nodes', 'nodesize'])):
    """Data structure for holding arbitrarily large numbers.

    Because python already supports arbitrarily large numbers, there isn't
    a practical need for this type. However, the assignment is asking us to
    make this data structure for learning purposes.

    Attributes:
        nodes (list of int): A list of symbolic digits for the data structure.
            Like any number system, the nodes represent one digit of the
            number. The maximum size of each node is determined by the BigInt's
            `nodesize`, which constrains the node's size to [0, 10^nodesize).

            The nodes are ordered from lowest value nodes to highest. For example,
            a number could be represented in the following form:

                155 #=> BigInt([5, 5, 1], 1)

        nodesize (int): The max size of each node, which constrains a node to
            the range [0, 10^nodesize].
    """
