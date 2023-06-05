#!/usr/bin/env python3
"""
A tetris board is 10 columns wide, indexed to 0-9

Rows drop as rows

The engine should model a grid that pieces enter from top and come to rest at the
bottom, as if pulled down by gravity. Each piece is made up of four unit squares. No
two unit squares can occupy the same space in the grid at the same time. The
pieces are rigid, and come to rest as soon as any part of a piece contacts the
bottom of the grid or any resting block. As in Tetris, whenever an entire row of the
grid is filled, it disappears, and any higher rows drop into the vacated space without
any change to the internal pattern of blocks in any row.

Your program must process a text file of lines each representing a sequence of
pieces entering the grid. For each line of the input file, your program should output
the resulting height of the remaining blocks within the grid.
"""

import argparse
from sys import stdin
from typing import List
import shapes


class Grid():
    """
    So let's talk about how grids work. We have a 2D array of squares, and we want to insert squares into the top of our grid.

    Now in real Tetris, they hard-code the number of rows and if you fill the grid, you fill the grid.

    But ours must be infinite bounded by our 128GB of RAM and 1TB Swap SSD.

    So the bottom row is row 0 and the top row is row N.  We want to insert squares into the top of our grid.
    """
    # Future cleanup, take this as an input
    ROW_WIDTH = 10

    # This can be almost anything, but in our codebase
    # 1. sum(s != EMPTY_SQUARE) == ROW_WIDTH to mean that the row is full
    # 2. all(s == EMPTY_SQUARE to mean that the row is empty
    # 3. s == EMPTY_SQUARE to mean that the square is empty
    #
    # So what I'm saying is that None cannot work here
    #
    # As a side note, I tend to play WAY crazier typing games in Python
    # with duck typing than I do in other languages
    # So our typing can support pretty much anything here
    EMPTY_SQUARE = 0

    def __init__(self) -> None:
        """
        Initialize the grid

        A grid is a list of list of rows and a list of tops which correspond to the highest point in each column
        """
        self.rows = []
        self.tops = [0] * self.ROW_WIDTH
        self.move_count = 0

    def __getitem__(self, item):
        """
        Subscribe to the grid like a list
        This currently doesn't do slices, but it could

        Possible bug for future me, if someone accidentally does grid[1,000,000], 
        it will allocate 1 Million empty rows
        """
        for _ in range(item - len(self.rows) + 1):
            self.rows.append(self.new_row())
        return self.rows[item]

    @classmethod
    def new_row(cls):
        """Return a new row that is empty and the correct width"""
        return [cls.EMPTY_SQUARE] * cls.ROW_WIDTH

    @classmethod
    def row_full(cls, row) -> bool:
        """Is the row full?"""
        return sum(x != cls.EMPTY_SQUARE for x in row) == cls.ROW_WIDTH

    @classmethod
    def row_empty(cls, row) -> bool:
        """Is the row empty?"""
        return all(x == cls.EMPTY_SQUARE for x in row) == cls.ROW_WIDTH

    def drop_shape(self, shape: shapes.Shape, column: int) -> None:
        """
        Given a grid, a new shape to add to the grid, and an input column, drop the shape into the grid
        """
        # For debugging, I find this to be a useful helper.
        # Where did these squares come from?
        self.move_count += 1

        # Figure out how high it's going
        drop_height = 0

        # A shape is a partial infill of a rectangular bounding box
        # So we need to find that bounding box using the highest point in each column
        # accounting for missing squares on the bottom of the shape
        for i in range(shape.width):
            col = column + i
            drop_height = max(drop_height, self.tops[col] - shape.bottoms[i])

        # Mark all the squares as full, creating new rows if needed
        for square in shape.squares:
            self[square[1] + drop_height][square[0] + column] = self.move_count

        # Scan every row that had new squares added to it to see if they're full or not
        # I'm doing it in reverse order because if I remove row 7, row 8 becomes row 7
        # And then when I remove row "8", I'm actually removing what used to be row 9
        # So we do this in reverse order to avoid that
        to_remove = []
        for row_index in range(
                drop_height + shape.height, drop_height - 1, -1):
            row = self[row_index]
            if self.row_full(row):
                to_remove.append(row_index)

        # If we don't need to remove any rows, we can add the shape to calculate the new tops array and be done
        # Otherwise, we need to account for the removed rows and recalculate
        # the tops array from scratch
        if not to_remove:
            # Update the tops array
            # It's the same idea as before, but we're accounting for missing
            # squares on the top of the shape now
            for i in range(shape.width):
                col = column + i
                self.tops[col] = max(
                    self.tops[col], shape.tops[i] + drop_height)
            return

        # assert to_remove and (to_remove == sorted(to_remove, reverse=True))
        for row_index in to_remove:
            self.rows.pop(row_index)

        # Then update the tops array
        for column_index in range(self.ROW_WIDTH):
            # Find the first row that's not empty
            for row_index in range(len(self.rows) - 1, -1, -1):
                if self[row_index][column_index] != self.EMPTY_SQUARE:
                    self.tops[column_index] = row_index + 1
                    break
            else:
                self.tops[column_index] = 0

    def highest(self) -> int:
        """
        return the maximum height of the rows with shapes in them for the grid
        """
        return max(self.tops)

    def get_rows(self) -> List[List]:
        """
        return a list of rows that are full
        """
        return self.rows[:self.highest()]

    def __str__(self) -> str:
        ###
        # This is a pretty-printer for the grid
        # It's not really important to the algorithm, but it's useful for debugging
        ###
        '''
        # For debugging purposes, I'm doing a neat little trick
        # For every move, the squares that were added are marked with the move number
        # So you can see where each square came from
        # So instead of scanning the whole grid to find the maximum move number, I'm just going to keep track of it
        # And that tells us the longest string representation of a move number
        # Which in turn I can then use to calculate the width of each square's representation
        # And then I can use that to right-justify each square
        # Taking Example 3 from the problem statement, your final grid output would be this
         - - 7 7 - - - - - -
         - - 7 7 - - - - - -
         1 1 - - 8 8 5 5 5 5
        '''
        if not self.highest():
            return "Empty grid"

        # I could do " ".join, but this is a deliberate choice to indent the grid by 1 space
        # Oddly, it's easier on my eyes to read
        square_len = len(str(self.move_count)) + 1

        def print_row(row):
            # https://www.tutorialspoint.com/how-to-get-a-string-left-padded-with-zeros-in-python
            return " ".join((str(x) if x else "-").rjust(square_len, " ")
                            for x in row)

        return "\n".join(
            print_row(
                self.rows[i]) for i in range(
                self.highest() - 1, -1, -1))


# Because I'm storing state as a grid object, I'm making a call to return
# None here
def process_line(grid: Grid, line: str, debug: bool = False) -> None:
    """
    Given a grid and a line of input, process the line of input into the grid
    """
    line = line.rstrip()
    for move in line.split(","):
        # All shapes are single-character
        shape_name, column = move[0], int(move[1:])
        shape = shapes.get_shape(shape_name)
        grid.drop_shape(shape, column)

        # This is a useful debugging tool
        if debug:
            print(shape_name, column)
            print(grid)
            print("Tops: " + str(grid.tops))
            print("Highest: " + str(grid.highest()))
            print()


def parse_args() -> argparse.Namespace:
    """I added an optional debug flag to help with debugging"""
    parser = argparse.ArgumentParser(description="Tetris solver for DRW")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    return parser.parse_args()


def main():
    """Main function"""
    debug = parse_args().debug
    for line in stdin:
        grid = Grid()
        process_line(grid, line, debug)
        print(grid.highest())


if __name__ == "__main__":
    main()
