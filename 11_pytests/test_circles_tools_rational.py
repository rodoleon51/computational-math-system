import pytest
from sympy import Rational, sqrt, simplify, symbols

from a_calculus.c_circles.circles_tools_rational import (
    distance_rational,
    point_circle_position_rational,
    center_radius_to_general_rational,
    general_to_center_radius_rational,
    line_circle_intersection_rational,
)

x, y = symbols("x y")

# ---------------------------------------------------------
# distance_rational
# ---------------------------------------------------------


def test_distance_rational_basic():
    assert simplify(distance_rational((0, 0), (3, 4)) - 5) == 0


def test_distance_rational_fractional():
    p1 = (Rational(1, 2), Rational(3, 2))
    p2 = (Rational(5, 2), Rational(7, 2))
    # Δx = 2, Δy = 2 -> Euclidean distance = 2*sqrt(2)
    assert simplify(distance_rational(p1, p2) - 2 * sqrt(2)) == 0


# ---------------------------------------------------------
# point_circle_position_rational
# ---------------------------------------------------------


def test_point_circle_position_rational_inside():
    assert point_circle_position_rational((0, 0), 5, (2, 1)) == -1


def test_point_circle_position_rational_on():
    assert point_circle_position_rational((0, 0), 5, (3, 4)) == 0


def test_point_circle_position_rational_outside():
    assert point_circle_position_rational((0, 0), 5, (6, 0)) == 1


# ---------------------------------------------------------
# center_radius_to_general_rational and back
# ---------------------------------------------------------


def test_center_radius_to_general_rational_and_back():
    center = (Rational(3), Rational(-2))
    radius = Rational(5)
    D, E, F = center_radius_to_general_rational(center, radius)
    h, k, r = general_to_center_radius_rational(D, E, F)
    assert simplify(h - center[0]) == 0
    assert simplify(k - center[1]) == 0
    assert simplify(r - radius) == 0


# ---------------------------------------------------------
# line_circle_intersection_rational
# ---------------------------------------------------------


def test_line_circle_intersection_rational_two_points():
    pts = line_circle_intersection_rational(0, 0, (0, 0), 5)
    assert len(pts) == 2
    assert simplify(pts[0][1]) == 0
    assert simplify(pts[1][1]) == 0


def test_line_circle_intersection_rational_tangent():
    pts = line_circle_intersection_rational(0, 5, (0, 0), 5)
    assert len(pts) == 1
    assert simplify(pts[0][1] - 5) == 0


def test_line_circle_intersection_rational_none():
    pts = line_circle_intersection_rational(0, 10, (0, 0), 5)
    assert pts == []


def test_line_circle_intersection_rational_fractional():
    pts = line_circle_intersection_rational(
        Rational(1, 2), Rational(1, 2), (Rational(1), Rational(1)), Rational(5, 2)
    )
    assert len(pts) == 2
    # Expected x-coordinates are 1 ± sqrt(5)
    expected_x1 = 1 + sqrt(5)
    expected_x2 = 1 - sqrt(5)
    # Order of points is not guaranteed; check both
    x_vals = [simplify(pts[0][0]), simplify(pts[1][0])]
    assert any(simplify(x - expected_x1) == 0 for x in x_vals)
    assert any(simplify(x - expected_x2) == 0 for x in x_vals)
