from sympy import sympify, simplify, sqrt, Expr, Number


def _to_sym(x):
    if isinstance(x, (Expr, Number)):
        return x
    return sympify(x)


def line_to_abc(eq, x, y):
    """
    Convert a SymPy equation (like x-3, y+4, 2*x-3*y+7) into (a, b, c)
    for ax + by + c = 0.
    """
    eq = sympify(eq)
    a = eq.coeff(x)
    b = eq.coeff(y)
    c = eq.subs({x: 0, y: 0})
    return a, b, c


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


def are_parallel(eq1, eq2, x, y):
    a1, b1, _ = line_to_abc(eq1, x, y)
    a2, b2, _ = line_to_abc(eq2, x, y)
    return simplify(a1 * b2 - a2 * b1) == 0


def are_perpendicular(eq1, eq2, x, y):
    a1, b1, _ = line_to_abc(eq1, x, y)
    a2, b2, _ = line_to_abc(eq2, x, y)
    return simplify(a1 * a2 + b1 * b2) == 0


def intersection_of_lines(m1, b1, m2, b2, x, y):
    m1, b1 = _to_sym(m1), _to_sym(b1)
    m2, b2 = _to_sym(m2), _to_sym(b2)

    # Convert slope-intercept form to general form: m*x - y + b = 0
    eq1 = m1 * x - y + b1
    eq2 = m2 * x - y + b2

    # Use the new general-form parallel test
    if are_parallel(eq1, eq2, x, y):
        raise ValueError("Lines are parallel; no intersection point.")

    # Solve normally (slope-intercept intersection)
    x_int = simplify((b2 - b1) / (m1 - m2))
    y_int = simplify(m1 * x_int + b1)

    return (x_int, y_int)
