"""
A separate module for shapes, shape lookup, and shape creation
"""
from collections import defaultdict


class Shape():
    """
    Shapes are defined by a list of squares and a list of bottoms
    Each square is a tuple of (x, y) coordinates defined as the offset from the lower left corner of the rectangle bounding the shape
    #ach bottom is a y coordinate defined as the offset from the bottom of
    the rectangle bounding the shape using the index of the list as a column
    index
    """

    def __init__(self, squares):
        self.squares = squares

        # Define the rectangle bounding the shape
        self.width = max(square[0] for square in squares) + 1
        self.height = max(square[1] for square in squares) + 1

        # Initialize the bottoms and tops
        # Bottom is the bottom of the lowest square in the column
        # Top is the top of the highest square in the column, ie: y-index + 1
        calc_bottoms = defaultdict(lambda: self.height)
        calc_tops = defaultdict(lambda: 0)
        for square in squares:
            calc_bottoms[square[0]] = min(calc_bottoms[square[0]], square[1])
            # NOTE THE +1 HERE
            calc_tops[square[0]] = max(calc_tops[square[0]], square[1] + 1)

        # convert these defaultdicts to lists
        self.bottoms = [calc_bottoms[i] for i in range(self.width)]
        self.tops = [calc_tops[i] for i in range(self.width)]


def get_shape(name):
    """
    The basic idea here is that we're going to define a bunch of global variables
    But our inputs are strings
    So this lets us lookup our global variables by string name

    https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
    """
    try:
        # We're being too tricky here, so we need to ensure we're only
        # returning Shapes
        ret = globals()[name]
        if isinstance(ret, Shape):
            return ret
        raise ValueError("Shape not found: " + name)
    except KeyError as exc:
        raise ValueError("Shape not found: " + name) from exc

# This is not alphabetical, but it's the order we were given
# in the input file which is in certain sublte ways more important

# pylint: disable=pointless-string-statement


"""
XX
XX
"""
Q = Shape([(0, 0), (0, 1), (1, 0), (1, 1)])

"""
-XX
XX-
"""
S = Shape([(0, 0), (1, 0), (1, 1), (2, 1)])

"""
XX-
-XX
"""
Z = Shape([(0, 1), (1, 1), (1, 0), (2, 0)])

"""
XXX
-X-
"""
T = Shape([(0, 1), (1, 1), (2, 1), (1, 0)])

"""
XXXX
"""
I = Shape([(0, 0), (1, 0), (2, 0), (3, 0)])

"""
X-
X-
XX
"""
L = Shape([(0, 0), (0, 1), (0, 2), (1, 0)])

"""
XX
X-
X-
"""
J = Shape([(0, 0), (1, 0), (1, 1), (1, 2)])
