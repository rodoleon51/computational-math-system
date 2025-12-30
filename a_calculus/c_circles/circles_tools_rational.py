from sympy import sympify, simplify, sqrt, Expr, Number

# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------


def _to_sym(x):
    if isinstance(x, (Expr, Number)):
        return x
    return sympify(x)


# ---------------------------------------------------------
# Basic circle utilities (symbolic)
# ---------------------------------------------------------


def distance_rational(p1, p2):
    """Exact Euclidean distance between two points."""
    x1, y1 = _to_sym(p1[0]), _to_sym(p1[1])
    x2, y2 = _to_sym(p2[0]), _to_sym(p2[1])
    return simplify(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def point_circle_position_rational(center, radius, point):
    """
    Determine if a point is inside, on, or outside a circle.
    Returns: -1 (inside), 0 (on), +1 (outside)
    """
    d = distance_rational(center, point)
    r = _to_sym(radius)
    diff = simplify(d - r)
    if diff == 0:
        return 0
    return -1 if diff < 0 else 1


def center_radius_to_general_rational(center, radius):
    """
    Convert (h, k), r to general form:
    x^2 + y^2 + D x + E y + F = 0
    """
    h, k = _to_sym(center[0]), _to_sym(center[1])
    r = _to_sym(radius)
    D = simplify(-2 * h)
    E = simplify(-2 * k)
    F = simplify(h * h + k * k - r * r)
    return (D, E, F)


def general_to_center_radius_rational(D, E, F):
    """
    Convert general form to center-radius form.
    """
    D, E, F = _to_sym(D), _to_sym(E), _to_sym(F)
    h = simplify(-D / 2)
    k = simplify(-E / 2)
    r = simplify(sqrt(h * h + k * k - F))
    return (h, k, r)


def line_circle_intersection_rational(m, b, center, radius):
    """
    Intersection of line y = m x + b with circle (h, k, r).
    Returns 0, 1, or 2 exact points.
    """
    m, b = _to_sym(m), _to_sym(b)
    h, k = _to_sym(center[0]), _to_sym(center[1])
    r = _to_sym(radius)

    # Substitute y = m x + b into circle equation
    A = simplify(sympify(1 + m*m))
    B = simplify(sympify(-2*h + 2*m*(b - k)))
    C = simplify(sympify(h*h + (b - k)**2 - r*r))
    disc = simplify(sympify(B*B - 4*A*C))


    disc = simplify(B * B - 4 * A * C)

    if disc < 0:
        return []
    elif disc == 0:
        x = simplify(-B / (2 * A))
        y = simplify(m * x + b)
        return [(x, y)]
    else:
        sqrt_disc = simplify(sqrt(disc))
        x1 = simplify((-B + sqrt_disc) / (2 * A))
        x2 = simplify((-B - sqrt_disc) / (2 * A))
        return [(x1, simplify(m * x1 + b)), (x2, simplify(m * x2 + b))]
