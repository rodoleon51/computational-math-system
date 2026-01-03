import pytest
from sympy import Rational, sqrt, Symbol, simplify
from a_calculus.utils.coordinates_tools_rational import (
    distance,
    midpoint,
    slope,
    point_slope,
    slope_intercept,
    quadrant,
)

# ---------------------------------------------------------
# distance()
# ---------------------------------------------------------


def test_distance_basic():
    assert simplify(distance((0, 0), (3, 4)) - 5) == 0


def test_distance_fractional():
    assert (
        simplify(
            distance((0, 0), (Rational(1, 2), Rational(3, 2)))
            - sqrt((Rational(1, 2)) ** 2 + (Rational(3, 2)) ** 2)
        )
        == 0
    )


def test_distance_negative():
    assert simplify(distance((-1, -1), (2, 3)) - sqrt(5**2)) == 0


# ---------------------------------------------------------
# midpoint()
# ---------------------------------------------------------


def test_midpoint_basic():
    assert midpoint((0, 0), (2, 2)) == (1, 1)


def test_midpoint_fractional():
    assert midpoint((1, Rational(1, 2)), (3, Rational(5, 2))) == (2, Rational(3, 2))


# ---------------------------------------------------------
# slope()
# ---------------------------------------------------------


def test_slope_basic():
    assert slope((1, 2), (3, 6)) == 2


def test_slope_fractional():
    assert slope((0, 0), (Rational(1, 2), Rational(3, 4))) == Rational(3, 2)


def test_slope_vertical_raises():
    with pytest.raises(ValueError):
        slope((2, 1), (2, 5))


# ---------------------------------------------------------
# point_slope()
# ---------------------------------------------------------


def test_point_slope_basic():
    # y - 2 = 2(x - 1) → at x=4, y = 8
    assert simplify(point_slope((1, 2), 2, 4) - 8) == 0


def test_point_slope_fractional():
    x = Symbol("x")
    expr = point_slope((0, 0), Rational(3, 4), x)
    assert simplify(expr - (Rational(3, 4) * x)) == 0


# ---------------------------------------------------------
# slope_intercept()
# ---------------------------------------------------------


def test_slope_intercept_basic():
    assert slope_intercept(2, 1, 4) == 9


def test_slope_intercept_fractional():
    assert slope_intercept(Rational(3, 2), Rational(1, 3), Rational(2, 3)) == simplify(
        Rational(3, 2) * Rational(2, 3) + Rational(1, 3)
    )


# ---------------------------------------------------------
# quadrant()
# ---------------------------------------------------------


def test_quadrant_q1():
    assert quadrant((3, 4)) == 1


def test_quadrant_q2():
    assert quadrant((-3, 4)) == 2


def test_quadrant_q3():
    assert quadrant((-3, -4)) == 3


def test_quadrant_q4():
    assert quadrant((3, -4)) == 4


def test_quadrant_axis():
    assert quadrant((0, 5)) == 0
    assert quadrant((3, 0)) == 0


# ---------------------------------------------------------
# validation tests
# ---------------------------------------------------------


def test_invalid_point_type():
    with pytest.raises(TypeError):
        distance("not a point", (1, 2))


def test_invalid_point_length():
    with pytest.raises(TypeError):
        distance((1,), (2, 3))


def test_invalid_number():
    with pytest.raises(TypeError):
        slope_intercept("a", 1, 2)
