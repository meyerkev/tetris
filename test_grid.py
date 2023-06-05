"""
Test the grid class and the process_line function
"""

# pylint: disable=missing-function-docstring,invalid-name

import shapes
import tetris


def test_empty():
    grid = tetris.Grid()
    assert grid.highest() == 0
    assert grid.get_rows() == []


def test_q():
    grid = tetris.Grid()
    grid.drop_shape(shapes.Q, 0)
    assert grid.highest() == 2


def test_q_with_i():
    grid = tetris.Grid()
    grid.drop_shape(shapes.Q, 0)
    assert grid.highest() == 2
    grid.drop_shape(shapes.I, 2)
    grid.drop_shape(shapes.I, 6)
    assert grid.highest() == 1
    grid.drop_shape(shapes.I, 2)
    grid.drop_shape(shapes.I, 6)
    assert grid.highest() == 0


def test_example1():
    g = tetris.Grid()
    tetris.process_line(g, "I0,I4,Q8")
    assert g.highest() == 1


def test_example2():
    g = tetris.Grid()
    tetris.process_line(g, "T1,Z3,I4")
    assert g.highest() == 4


def test_example3():
    g = tetris.Grid()
    tetris.process_line(g, "Q0,I2,I6,I0,I6,I6,Q2,Q4")
    assert g.highest() == 3


def test_missing_upper_line():
    """
    Create a situation that lets you remove one line above the zero and test that this works
    """
    # Drop a Z and an S
    g = tetris.Grid()
    g.drop_shape(shapes.S, 1)
    g.drop_shape(shapes.Z, 4)
    assert g.highest() == 2

    # Drop a Q and an I
    g.drop_shape(shapes.Q, 0)
    assert g.highest() == 3

    g.drop_shape(shapes.I, 6)
    # Because we blew away the missing line
    assert g.highest() == 2

    # drop two more I's
    g.drop_shape(shapes.I, 2)
    g.drop_shape(shapes.I, 6)
    assert g.highest() == 1


def test_open():
    # Drop a Z and an S
    g = tetris.Grid()
    g.drop_shape(shapes.S, 1)
    g.drop_shape(shapes.Z, 4)
    print(g)
    print()

    g.drop_shape(shapes.L, 0)
    g.drop_shape(shapes.J, 8)
    print(g)

    assert g.highest() == 4

    g.drop_shape(shapes.T, 6)
    assert g.highest() == 3


def test_single_shapes():
    g = tetris.Grid()
    g.drop_shape(shapes.Q, 0)
    assert g.highest() == 2

    g = tetris.Grid()
    g.drop_shape(shapes.S, 0)
    assert g.highest() == 2

    g = tetris.Grid()
    g.drop_shape(shapes.Z, 0)
    assert g.highest() == 2

    g = tetris.Grid()
    g.drop_shape(shapes.T, 0)
    assert g.highest() == 2

    g = tetris.Grid()
    g.drop_shape(shapes.I, 0)
    assert g.highest() == 1

    g = tetris.Grid()
    g.drop_shape(shapes.L, 0)
    assert g.highest() == 3

    g = tetris.Grid()
    g.drop_shape(shapes.J, 0)
    assert g.highest() == 3


def test_stack_every_shape():
    g = tetris.Grid()
    g.drop_shape(shapes.Q, 0)
    assert g.highest() == 2
    g.drop_shape(shapes.S, 0)
    assert g.highest() == 4
    g.drop_shape(shapes.Z, 0)
    assert g.highest() == 6
    g.drop_shape(shapes.T, 0)
    assert g.highest() == 8
    g.drop_shape(shapes.I, 0)
    assert g.highest() == 9
    g.drop_shape(shapes.L, 0)
    assert g.highest() == 12
    g.drop_shape(shapes.J, 0)
    assert g.highest() == 15


def test_stack_s_z():
    g = tetris.Grid()
    g.drop_shape(shapes.S, 2)
    assert g.highest() == 2
    g.drop_shape(shapes.Z, 0)
    assert g.highest() == 3


def test_stack_z_s():
    g2 = tetris.Grid()
    g2.drop_shape(shapes.Z, 0)
    assert g2.highest() == 2
    g2.drop_shape(shapes.S, 2)
    assert g2.highest() == 3


def test_stack_s_z_repeatedly():
    pass


def test_stack_z_i():
    g3 = tetris.Grid()
    g3.drop_shape(shapes.Z, 0)
    assert g3.highest() == 2
    g3.drop_shape(shapes.I, 2)
    assert g3.highest() == 2


def test_stack_i_s():
    g4 = tetris.Grid()
    g4.drop_shape(shapes.I, 2)
    assert g4.highest() == 1
    g4.drop_shape(shapes.S, 0)
    assert g4.highest() == 2


def test_stack_i_z():
    g = tetris.Grid()
    g.drop_shape(shapes.I, 0)
    assert g.highest() == 1
    g.drop_shape(shapes.Z, 2)
    assert g.highest() == 3

    g2 = tetris.Grid()
    g2.drop_shape(shapes.I, 0)
    assert g2.highest() == 1
    g2.drop_shape(shapes.Z, 3)
    assert g2.highest() == 2


def test_stack_t():
    g = tetris.Grid()
    g.drop_shape(shapes.T, 0)
    assert g.highest() == 2
    g.drop_shape(shapes.T, 2)
    assert g.highest() == 3
    g.drop_shape(shapes.T, 4)
    assert g.highest() == 4
    g.drop_shape(shapes.T, 6)
    assert g.highest() == 5


def test_stack_s():
    g = tetris.Grid()
    height = 2
    for i in range(tetris.Grid.ROW_WIDTH - shapes.S.width - 1, -1, -1):
        g.drop_shape(shapes.S, i)
        assert g.highest() == height
        height += 1


def test_stack_z():
    g = tetris.Grid()
    height = 2
    for i in range(tetris.Grid.ROW_WIDTH - shapes.Z.width):
        g.drop_shape(shapes.Z, i)
        assert g.highest() == height
        height += 1


def test_stack_z_t():
    g = tetris.Grid()
    g.drop_shape(shapes.Z, 0)
    assert g.highest() == 2
    g.drop_shape(shapes.T, 2)
    assert g.highest() == 2

    g2 = tetris.Grid()
    g2.drop_shape(shapes.Z, 2)
    g2.drop_shape(shapes.T, 0)
    print(g2)
    assert g2.highest() == 3


def test_stack_t_s():
    g = tetris.Grid()
    g.drop_shape(shapes.S, 2)
    assert g.highest() == 2
    g.drop_shape(shapes.T, 0)
    assert g.highest() == 2

    g2 = tetris.Grid()
    g2.drop_shape(shapes.S, 2)
    g2.drop_shape(shapes.T, 1)
    assert g2.highest() == 3


SAMPLE_INPUT = """
Q0
Q0,Q1
Q0,Q2,Q4,Q6,Q8
Q0,Q2,Q4,Q6,Q8,Q1
Q0,Q2,Q4,Q6,Q8,Q1,Q1
I0,I4,Q8
I0,I4,Q8,I0,I4
L0,J2,L4,J6,Q8
L0,Z1,Z3,Z5,Z7
T0,T3
T0,T3,I6,I6
I0,I6,S4
T1,Z3,I4
L0,J3,L5,J8,T1
L0,J3,L5,J8,T1,T6
L0,J3,L5,J8,T1,T6,J2,L6,T0,T7
L0,J3,L5,J8,T1,T6,J2,L6,T0,T7,Q4
S0,S2,S4,S6
S0,S2,S4,S5,Q8,Q8,Q8,Q8,T1,Q1,I0,Q4
L0,J3,L5,J8,T1,T6,S2,Z5,T0,T7
Q0,I2,I6,I0,I6,I6,Q2,Q4
""".strip().split("\n")

ANSWERS = [
    2,
    4,
    0,
    2,
    4,
    1,
    0,
    2,
    2,
    2,
    1,
    1,
    4,
    3,
    1,
    2,
    1,
    8,
    8,
    0,
    3,
]


def test_sample_input():
    for line, expected_result in zip(SAMPLE_INPUT, ANSWERS):
        g = tetris.Grid()
        tetris.process_line(g, line)
        assert g.highest() == expected_result
