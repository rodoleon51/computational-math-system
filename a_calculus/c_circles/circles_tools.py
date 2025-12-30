import math

# ---------------------------------------------------------
# Basic circle utilities (numeric)
# ---------------------------------------------------------


def distance_numeric(p1, p2):
    """Euclidean distance between two points (numeric)."""
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


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
