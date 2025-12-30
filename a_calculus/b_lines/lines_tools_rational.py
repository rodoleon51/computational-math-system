from sympy import sympify, simplify, sqrt, Expr, Number


def _to_sym(x):
    if isinstance(x, (Expr, Number)):
        return x
    return sympify(x)


def slope(p1, p2):
    x1, y1 = _to_sym(p1[0]), _to_sym(p1[1])
    x2, y2 = _to_sym(p2[0]), _to_sym(p2[1])
    if x1 == x2:
        raise ValueError("Slope undefined for vertical lines.")
    return simplify((y2 - y1) / (x2 - x1))


def intercept_from_point_slope(p, m):
    x0, y0 = _to_sym(p[0]), _to_sym(p[1])
    m = _to_sym(m)
    return simplify(y0 - m * x0)


def line_equation_two_points(p1, p2):
    m = slope(p1, p2)
    b = intercept_from_point_slope(p1, m)
    return m, b


def distance_point_to_line(p, m, b):
    x0, y0 = _to_sym(p[0]), _to_sym(p[1])
    m, b = _to_sym(m), _to_sym(b)
    expr = sympify(abs(m * x0 - y0 + b) / sqrt(m**2 + 1))
    return simplify(expr)


def are_parallel(m1, m2):
    return simplify(_to_sym(m1) - _to_sym(m2)) == 0


def are_perpendicular(m1, m2):
    return simplify(_to_sym(m1) * _to_sym(m2) + 1) == 0

def intersection_of_lines(m1, b1, m2, b2):
    m1, b1 = _to_sym(m1), _to_sym(b1)
    m2, b2 = _to_sym(m2), _to_sym(b2)

    if are_parallel(m1, m2):
        raise ValueError("Lines are parallel; no intersection point.")

    x = simplify((b2 - b1) / (m1 - m2))
    y = simplify(m1 * x + b1)
    return (x, y)
