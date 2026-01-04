import math

# ---------------------------------------------------------
# Basic circle utilities (numeric)
# ---------------------------------------------------------


def distance_numeric(p1, p2):
    """Euclidean distance between two points (numeric)."""
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def detect_and_normalize_circle_numeric(A, B, C, D, E, F, tol=1e-9):
    """
    Numeric version of circle detection and normalization.

    Returns:
        (True, (D_norm, E_norm, F_norm)) if circle
        (False, None) if not a circle
    """

    # Must have quadratic terms
    if abs(A) < tol and abs(C) < tol:
        return (False, None)

    # No xy term allowed
    if abs(B) > tol:
        return (False, None)

    # Must have equal coefficients for x^2 and y^2
    if abs(A - C) > tol:
        return (False, None)

    # Normalize if needed
    if abs(A - 1.0) > tol:
        Dn = D / A
        En = E / A
        Fn = F / A
    else:
        Dn, En, Fn = D, E, F

    return (True, (Dn, En, Fn))


import math


def circle_from_center_point_numeric(center, point):
    """
    Numeric version: center (h, k) and point (x1, y1) → (h, k, r)
    """
    h, k = center
    x1, y1 = point
    r = math.sqrt((x1 - h) ** 2 + (y1 - k) ** 2)
    return (h, k, r)


def standard_equation_from_center_radius_numeric(center, radius):
    """
    Return the standard equation (x - h)^2 + (y - k)^2 = r^2
    as a formatted string using numeric values.
    """
    h, k = center
    r = radius

    eq_str = f"(x - {h})^2 + (y - {k})^2 = {r**2}"
    return eq_str


def circle_from_center_point_radius_numeric(center, point, radius, tol=1e-9):
    """
    Numeric version with tolerance checking.
    """
    h, k = center
    x1, y1 = point
    r = float(radius)

    dist = math.sqrt((x1 - h) ** 2 + (y1 - k) ** 2)
    if abs(dist - r) > tol:
        raise ValueError("Point is not at distance r from center.")

    return (h, k, r)


def point_circle_position(center, radius, point):
    """
    Determine if a point is inside, on, or outside a circle.
    Returns: -1 (inside), 0 (on), +1 (outside)
    """
    d = distance_numeric(center, point)
    if abs(d - radius) < 1e-9:
        return 0
    return -1 if d < radius else 1


def center_radius_to_general(center, radius):
    """
    Convert (h, k), r to general form:
    x^2 + y^2 + Dx + Ey + F = 0
    """
    h, k = center
    D = -2 * h
    E = -2 * k
    F = h * h + k * k - radius * radius
    return (D, E, F)


def general_to_center_radius(D, E, F):
    """
    Convert general form to center-radius form.
    """
    h = -D / 2
    k = -E / 2
    r = math.sqrt(h * h + k * k - F)
    return (h, k, r)


def line_circle_intersection_numeric(m, b, center, radius):
    """
    Intersection of line y = m x + b with circle (h, k, r).
    Returns 0, 1, or 2 points.
    """
    h, k = center
    # Substitute y = m x + b into circle equation
    # (x - h)^2 + (m x + b - k)^2 = r^2
    A = 1 + m * m
    B = -2 * h + 2 * m * (b - k)
    C = h * h + (b - k) ** 2 - radius * radius

    disc = B * B - 4 * A * C
    if disc < 0:
        return []
    elif abs(disc) < 1e-9:
        x = -B / (2 * A)
        y = m * x + b
        return [(x, y)]
    else:
        sqrt_disc = math.sqrt(disc)
        x1 = (-B + sqrt_disc) / (2 * A)
        x2 = (-B - sqrt_disc) / (2 * A)
        return [(x1, m * x1 + b), (x2, m * x2 + b)]
