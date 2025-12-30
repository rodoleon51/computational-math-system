import pytest
from sympy import Rational, simplify, symbols

from a_calculus.b_lines.lines_tools_rational import (
    slope,
    intercept_from_point_slope,
    line_equation_two_points,
    distance_point_to_line,
    are_parallel,
    are_perpendicular,
)

x, y = symbols("x y")

# ---------------------------------------------------------
# slope
# ---------------------------------------------------------


def test_slope_rational_basic():
    assert slope((1, 2), (3, 6)) == 2


def test_slope_rational_fractional():
    m = slope((0, 0), (Rational(1, 2), Rational(3, 4)))
    assert m == Rational(3, 2)


def test_slope_rational_vertical():
    with pytest.raises(ValueError):
        slope((2, 1), (2, 5))


# ---------------------------------------------------------
# intercept_from_point_slope
# ---------------------------------------------------------


def test_intercept_from_point_slope_rational():
    b = intercept_from_point_slope((1, 3), Rational(2))
    assert b == 1


# ---------------------------------------------------------
# line_equation_two_points
# ---------------------------------------------------------


def test_line_equation_two_points_rational():
    m, b = line_equation_two_points((1, 2), (3, 6))
    assert m == 2
    assert b == 0


# ---------------------------------------------------------
# distance_point_to_line
# ---------------------------------------------------------


def test_distance_point_to_line_rational():
    d = distance_point_to_line((0, 0), Rational(2), Rational(1))
    assert simplify(d - Rational(1, 5) ** Rational(1, 2)) == 0


# ---------------------------------------------------------
# are_parallel / are_perpendicular (general form)
# ---------------------------------------------------------


def test_are_parallel_rational():
    # x - 3 = 0  (vertical)
    eq1 = x - 3
    # x - 7 = 0  (vertical)
    eq2 = x - 7
    assert are_parallel(eq1, eq2, x, y)


def test_are_perpendicular_rational():
    # x = 3  → x - 3 = 0
    eq1 = x - 3
    # y = -4 → y + 4 = 0
    eq2 = y + 4
    assert are_perpendicular(eq1, eq2, x, y)
