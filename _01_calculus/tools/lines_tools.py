import math


def slope(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2:
        raise ValueError("Slope undefined for vertical lines.")
    return (y2 - y1) / (x2 - x1)


def intercept_from_point_slope(p, m):
    x0, y0 = p
    return y0 - m * x0


def line_equation_two_points(p1, p2):
    m = slope(p1, p2)
    b = intercept_from_point_slope(p1, m)
    return m, b


def distance_point_to_line(p, m, b):
    x0, y0 = p
    return abs(m * x0 - y0 + b) / math.sqrt(m**2 + 1)


def are_parallel(m1, m2):
    return m1 == m2


def are_perpendicular(m1, m2):
    return m1 * m2 == -1
