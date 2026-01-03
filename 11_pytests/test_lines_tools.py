import pytest
from a_calculus.b_lines.lines_tools import (
    slope,
    intercept_from_point_slope,
    line_equation_two_points,
    distance_point_to_line,
    are_parallel,
    are_perpendicular,
)

# ---------------------------------------------------------
# slope
# ---------------------------------------------------------


def test_slope_basic():
    assert slope((1, 2), (3, 6)) == 2


def test_slope_negative():
    assert slope((0, 0), (2, -4)) == -2


def test_slope_vertical_raises():
    with pytest.raises(ValueError):
        slope((2, 1), (2, 5))


# ---------------------------------------------------------
# intercept_from_point_slope
# ---------------------------------------------------------


def test_intercept_from_point_slope():
    # y - 3 = 2(x - 1) → y = 2x + 1
    assert intercept_from_point_slope((1, 3), 2) == 1


# ---------------------------------------------------------
# line_equation_two_points
# ---------------------------------------------------------


def test_line_equation_two_points():
    m, b = line_equation_two_points((1, 2), (3, 6))
    assert m == 2
    assert b == 0


# ---------------------------------------------------------
# distance_point_to_line
# ---------------------------------------------------------


def test_distance_point_to_line():
    # Distance from (0,0) to y = 2x + 1
    d = distance_point_to_line((0, 0), 2, 1)
    assert abs(d - 1 / (5**0.5)) < 1e-9


# ---------------------------------------------------------
# are_parallel / are_perpendicular
# ---------------------------------------------------------


def test_are_parallel():
    assert are_parallel(2, 2)
    assert not are_parallel(2, -1 / 2)


def test_are_perpendicular():
    assert are_perpendicular(2, -1 / 2)
    assert not are_perpendicular(2, 2)
