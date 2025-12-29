import math


def distance(p1, p2):
    """Return the Euclidean distance between two points."""
    _validate_point(p1)
    _validate_point(p2)
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def midpoint(p1, p2):
    """Return the midpoint of two points."""
    _validate_point(p1)
    _validate_point(p2)
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def slope(p1, p2):
    """Return the slope of the line through two points."""
    _validate_point(p1)
    _validate_point(p2)
    if p2[0] == p1[0]:
        raise ValueError("Slope is undefined for vertical lines.")
    return (p2[1] - p1[1]) / (p2[0] - p1[0])


def point_slope(p, m, x):
    """Return y using the point–slope formula: y - y1 = m(x - x1)."""
    _validate_point(p)
    _validate_number(m)
    _validate_number(x)
    return p[1] + m * (x - p[0])


def slope_intercept(m, b, x):
    """Return y using the slope–intercept formula: y = mx + b."""
    _validate_number(m)
    _validate_number(b)
    _validate_number(x)
    return m * x + b


def quadrant(p):
    """Return the quadrant number (1–4) or 0 if the point lies on an axis."""
    _validate_point(p)
    x, y = p
    if x == 0 or y == 0:
        return 0
    if x > 0 and y > 0:
        return 1
    if x < 0 and y > 0:
        return 2
    if x < 0 and y < 0:
        return 3
    return 4


# -------------------------
# Internal validation tools
# -------------------------


def _validate_point(p):
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        raise TypeError("Point must be a tuple or list of length 2.")
    _validate_number(p[0])
    _validate_number(p[1])


def _validate_number(x):
    if not isinstance(x, (int, float)):
        raise TypeError("Value must be numeric.")
