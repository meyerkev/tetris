# The problem statement as presented

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

For more information, see TetrisProgrammingExercise.pdf

## To run

```
./tetris.py <my_input.txt >my_output.txt

# Or if for some reason, /usr/bin/env doesn't work
python3 ./tetris3.py <my_input.txt >my_output.txt
```