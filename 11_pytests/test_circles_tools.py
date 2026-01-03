import math
import pytest

from a_calculus.c_circles.circles_tools import (
    distance_numeric,
    point_circle_position,
    center_radius_to_general,
    general_to_center_radius,
    line_circle_intersection_numeric,
)

# ---------------------------------------------------------
# distance_numeric
# ---------------------------------------------------------


def test_distance_numeric_basic():
    assert abs(distance_numeric((0, 0), (3, 4)) - 5) < 1e-9


def test_distance_numeric_fractional():
    assert abs(distance_numeric((1.5, 2.5), (4.5, 6.5)) - 5) < 1e-9


# ---------------------------------------------------------
# point_circle_position
# ---------------------------------------------------------


def test_point_circle_position_inside():
    assert point_circle_position((0, 0), 5, (2, 1)) == -1


def test_point_circle_position_on():
    assert point_circle_position((0, 0), 5, (3, 4)) == 0


def test_point_circle_position_outside():
    assert point_circle_position((0, 0), 5, (6, 0)) == 1


# ---------------------------------------------------------
# center_radius_to_general and general_to_center_radius
# ---------------------------------------------------------


def test_center_radius_to_general_and_back():
    center = (3, -2)
    radius = 5
    D, E, F = center_radius_to_general(center, radius)
    h, k, r = general_to_center_radius(D, E, F)
    assert abs(h - center[0]) < 1e-9
    assert abs(k - center[1]) < 1e-9
    assert abs(r - radius) < 1e-9


# ---------------------------------------------------------
# line_circle_intersection_numeric
# ---------------------------------------------------------


def test_line_circle_intersection_two_points():
    # Circle: center (0,0), r=5
    # Line: y = 0 (horizontal)
    pts = line_circle_intersection_numeric(0, 0, (0, 0), 5)
    assert len(pts) == 2
    assert abs(pts[0][1]) < 1e-9
    assert abs(pts[1][1]) < 1e-9


def test_line_circle_intersection_tangent():
    # Circle: center (0,0), r=5
    # Line: y = 5 (tangent)
    pts = line_circle_intersection_numeric(0, 5, (0, 0), 5)
    assert len(pts) == 1
    assert abs(pts[0][1] - 5) < 1e-9


def test_line_circle_intersection_none():
    # Circle: center (0,0), r=5
    # Line: y = 10 (no intersection)
    pts = line_circle_intersection_numeric(0, 10, (0, 0), 5)
    assert pts == []
