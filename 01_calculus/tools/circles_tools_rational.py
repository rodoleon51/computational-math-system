"""
circles_tools_rational.py

Exact (rational/symbolic) circle utilities using SymPy.

Design notes
- Keep "representation" separate from "printing":
  * general form can be expanded safely
  * standard form should be kept as (h, k, r2) to preserve structure
- Prefer SymPy objects everywhere; convert inputs with _to_sym().
"""

from __future__ import annotations

import sympy as sp

# Public symbols (useful for building expressions)
x, y = sp.symbols("x y")

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _to_sym(val):
    """Convert Python scalars/strings to SymPy objects (leave SymPy alone)."""
    if isinstance(val, sp.Basic):
        return val
    return sp.sympify(val)

def _to_rational(val):
    """Best-effort exact conversion: ints -> Rational, floats -> nsimplify."""
    if isinstance(val, (int, sp.Integer, sp.Rational)):
        return sp.Rational(val)
    return sp.nsimplify(val)

def _cmp_to_zero(expr):
    """
    Compare a SymPy expression to 0 when possible.
    Returns -1, 0, +1 for negative/zero/positive.
    Raises ValueError if sign cannot be determined (symbolic/ambiguous).
    """
    expr = sp.simplify(expr)

    if expr == 0:
        return 0

    # Prefer SymPy's sign knowledge first
    if expr.is_number:
        s = sp.sign(expr)
        if s == 0:
            return 0
        return -1 if s < 0 else 1

    # Sometimes SymPy can infer sign
    if expr.is_positive is True:
        return 1
    if expr.is_negative is True:
        return -1

    raise ValueError(f"Cannot determine sign of expression: {expr!s}")

# ---------------------------------------------------------
# Pretty printing
# ---------------------------------------------------------

def _fmt_shift(var: str, a):
    """Format (var - a) with clean signs."""
    a = sp.simplify(a)
    if a == 0:
        return var
    if a.is_number and a < 0:
        return f"{var} + {sp.simplify(-a)}"
    return f"{var} - {a}"

def pretty_standard_circle(h, k, r2):
    """
    Textbook string: (x - h)^2 + (y - k)^2 = r^2
    Uses r2 directly (so you don't get '(r)^2' clutter).
    """
    h, k, r2 = map(sp.simplify, (_to_sym(h), _to_sym(k), _to_sym(r2)))
    left = f"({_fmt_shift('x', h)})^2 + ({_fmt_shift('y', k)})^2"
    return f"{left} = {r2}"

# ---------------------------------------------------------
# Core geometry
# ---------------------------------------------------------

def distance_rational(p1, p2):
    """Exact Euclidean distance between two points."""
    x1, y1 = map(_to_sym, p1)
    x2, y2 = map(_to_sym, p2)
    return sp.simplify(sp.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

def detect_and_normalize_circle_rational(A, B, C, D, E, F):
    """
    Detect whether A x^2 + B x y + C y^2 + D x + E y + F = 0 is a circle.
    If so, normalize to x^2 + y^2 + Dn x + En y + Fn = 0.

    Returns:
      (True, (Dn, En, Fn)) or (False, None)
    """
    A, B, C, D, E, F = map(_to_sym, (A, B, C, D, E, F))

    # Must have quadratic terms
    if A == 0 and C == 0:
        return (False, None)

    # No xy term allowed (in standard Cartesian axes)
    if sp.simplify(B) != 0:
        return (False, None)

    # Must have equal coefficients for x^2 and y^2
    if sp.simplify(A - C) != 0:
        return (False, None)

    # Normalize
    if A != 1:
        Dn = sp.simplify(D / A)
        En = sp.simplify(E / A)
        Fn = sp.simplify(F / A)
    else:
        Dn, En, Fn = D, E, F

    return (True, (Dn, En, Fn))

def general_to_center_radius_rational(D, E, F):
    """Convert x^2 + y^2 + D x + E y + F = 0 to (h, k, r) exactly."""
    D, E, F = map(_to_sym, (D, E, F))
    h = sp.simplify(-D / 2)
    k = sp.simplify(-E / 2)
    r2 = sp.simplify(h*h + k*k - F)
    r = sp.sqrt(r2)
    return (h, k, r, r2)

def center_radius_to_general_rational(center, radius):
    """Convert (h,k), r to (D,E,F) for x^2 + y^2 + D x + E y + F = 0."""
    h, k = map(_to_sym, center)
    r = _to_sym(radius)
    D = sp.simplify(-2 * h)
    E = sp.simplify(-2 * k)
    F = sp.simplify(h*h + k*k - r*r)
    return (D, E, F)

def circle_from_center_point_rational(center, point):
    """Given center (h,k) and a point on circle, return (h,k,r,r2) exactly."""
    h, k = map(_to_sym, center)
    x1, y1 = map(_to_sym, point)
    r2 = sp.simplify((x1 - h) ** 2 + (y1 - k) ** 2)
    r = sp.sqrt(r2)
    return (h, k, r, r2)

def standard_equation_from_center_radius_rational(center, radius):
    """
    Return:
      - expr0 : (x-h)^2 + (y-k)^2 - r^2 (as expression == 0)
      - pretty: '(x - h)^2 + (y - k)^2 = r^2' (clean signs)
    """
    h, k = map(_to_sym, center)
    r = _to_sym(radius)
    r2 = sp.simplify(r*r)
    expr0 = sp.simplify((x - h) ** 2 + (y - k) ** 2 - r2)
    return expr0, pretty_standard_circle(h, k, r2)

def circle_from_3_points_rational(p1, p2, p3):
    """
    Exact circle through 3 points.
    Returns center, radius, radius_sq, general expression, and a pretty standard string.
    """
    (x1, y1) = map(_to_rational, p1)
    (x2, y2) = map(_to_rational, p2)
    (x3, y3) = map(_to_rational, p3)

    D, E, F = sp.symbols("D E F")

    eqs = [
        x1**2 + y1**2 + D*x1 + E*y1 + F,
        x2**2 + y2**2 + D*x2 + E*y2 + F,
        x3**2 + y3**2 + D*x3 + E*y3 + F,
    ]

    sol = sp.solve(eqs, (D, E, F), dict=True)
    if not sol:
        raise ValueError("Points are collinear — no unique circle.")

    Dv, Ev, Fv = sol[0][D], sol[0][E], sol[0][F]

    h = sp.simplify(-Dv / 2)
    k = sp.simplify(-Ev / 2)
    r2 = sp.simplify(h*h + k*k - Fv)
    r = sp.sqrt(r2)

    general_eq = sp.expand(x**2 + y**2 + Dv*x + Ev*y + Fv)

    return {
        "center": (h, k),
        "radius_sq": r2,
        "radius": r,
        "D": Dv, "E": Ev, "F": Fv,
        "general_eq": general_eq,          # safe to expand
        "standard_tuple": (h, k, r2),      # preserve structure
        "standard_str": pretty_standard_circle(h, k, r2),
    }

def circle_from_center_point_radius_rational(center, point, radius):
    """Verify point lies on circle and return (h,k,r,r2) exactly."""
    h, k = map(_to_sym, center)
    x1, y1 = map(_to_sym, point)
    r = _to_sym(radius)

    dist = sp.simplify(sp.sqrt((x1 - h) ** 2 + (y1 - k) ** 2))
    if sp.simplify(dist - r) != 0:
        raise ValueError("Point is not at distance r from center.")
    return (h, k, r, sp.simplify(r*r))

def point_circle_position_rational(center, radius, point):
    """
    Inside/on/outside test. Returns -1, 0, +1.

    Note: For symbolic inputs where sign can't be determined, raises ValueError.
    """
    d = distance_rational(center, point)
    r = _to_sym(radius)
    return _cmp_to_zero(d - r)

def line_circle_intersection_rational(m, b, center, radius):
    """
    Intersection of y = m x + b with circle (h,k,r).

    Returns 0, 1, or 2 points, exact when inputs are exact.
    Robust for both numeric and symbolic m,b (within SymPy's abilities).
    """
    m, b = map(_to_sym, (m, b))
    h, k = map(_to_sym, center)
    r = _to_sym(radius)

    # Circle equation: (x-h)^2 + (y-k)^2 = r^2 with y = m x + b
    y_sub = m*x + b
    poly = sp.expand((x - h)**2 + (y_sub - k)**2 - r*r)

    # Solve for x
    xs = sp.solve(sp.Eq(poly, 0), x)
    pts = []
    for xv in xs:
        yv = sp.simplify(m*xv + b)
        pts.append((sp.simplify(xv), yv))

    # Remove duplicates (can happen with symbolic solve)
    uniq = []
    for p in pts:
        if p not in uniq:
            uniq.append(p)
    return uniq
