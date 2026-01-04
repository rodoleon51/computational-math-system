"""
circles_tools_rational.py

Exact (rational/symbolic) circle utilities using SymPy.

Goals
-----
1) Math correctness (exact arithmetic when possible).
2) Notebook-friendly: keep "standard form" structured for clean printing.
3) Type-checker friendly (VSCode Pylance/Pyright): use Expr-returning helpers.

Conventions
-----------
- General (expanded) form:
    x^2 + y^2 + D x + E y + F = 0
- Standard (structured) form:
    center (h,k), radius^2 = r2
    (x - h)^2 + (y - k)^2 = r2
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple, Union, cast

import sympy as sp
from sympy.core.expr import Expr

# Public symbols (handy for building expressions)
x, y = sp.symbols("x y")


# ---------------------------------------------------------------------
# Helpers (type-checker friendly)
# ---------------------------------------------------------------------

def _to_expr(val: Any) -> Expr:
    """Convert a Python value to a SymPy Expr (best effort)."""
    if isinstance(val, Expr):
        return val
    # sympify returns Basic, but in practice it's an Expr for numeric/string input;
    # cast keeps static type-checkers happy.
    return cast(Expr, sp.sympify(val))


def _to_rational_expr(val: Any) -> Expr:
    """
    Best-effort exact conversion:
    - ints -> Rational
    - SymPy Integer/Rational -> unchanged
    - floats/strings -> nsimplify (may produce Rational or algebraic Expr)
    """
    if isinstance(val, (int, sp.Integer, sp.Rational)):
        return cast(Expr, sp.Rational(val))
    return cast(Expr, sp.nsimplify(val))


def _sign_known(expr: Expr) -> int:
    """
    Determine sign of expr when possible.
    Returns: -1 (negative), 0 (zero), +1 (positive)
    Raises ValueError if sign cannot be decided symbolically.
    """
    expr = sp.simplify(expr)

    if expr == 0:
        return 0

    if expr.is_number:
        s = sp.sign(expr)
        if s == 0:
            return 0
        return -1 if s < 0 else 1

    if expr.is_positive is True:
        return 1
    if expr.is_negative is True:
        return -1

    raise ValueError(f"Cannot determine sign of expression: {expr}")


# ---------------------------------------------------------------------
# Pretty printing
# ---------------------------------------------------------------------

def _fmt_shift(var: str, a: Expr) -> str:
    """Format 'x - a' with clean signs: x, x - 3, x + 3, x - 5/2, ..."""
    a = sp.simplify(_to_expr(a))
    if a == 0:
        return var
    # Avoid symbolic comparisons; use SymPy sign flags when known.
    if a.is_negative is True:
        return f"{var} + {sp.simplify(-a)}"
    return f"{var} - {a}"


def pretty_standard_circle(h: Any, k: Any, r2: Any) -> str:
    """
    Textbook string:
        (x - h)^2 + (y - k)^2 = r^2
    Uses r2 directly (so you get '= 100', not '= (10)^2').
    """
    h_e, k_e, r2_e = map(lambda v: sp.simplify(_to_expr(v)), (h, k, r2))
    left = f"({_fmt_shift('x', h_e)})^2 + ({_fmt_shift('y', k_e)})^2"
    return f"{left} = {r2_e}"


# ---------------------------------------------------------------------
# Core circle conversions
# ---------------------------------------------------------------------

def detect_and_normalize_circle_rational(
    A: Any, B: Any, C: Any, D: Any, E: Any, F: Any
) -> Tuple[bool, Union[Tuple[Expr, Expr, Expr], None]]:
    """
    Detect if the conic
        A x^2 + B x y + C y^2 + D x + E y + F = 0
    represents a circle (in standard axes), and normalize to:
        x^2 + y^2 + Dn x + En y + Fn = 0

    Returns:
      (True, (Dn, En, Fn)) or (False, None)
    """
    A_e, B_e, C_e, D_e, E_e, F_e = map(_to_expr, (A, B, C, D, E, F))

    # Must have quadratic terms
    if sp.simplify(A_e) == 0 and sp.simplify(C_e) == 0:
        return (False, None)

    # No xy term for an axis-aligned circle
    if sp.simplify(B_e) != 0:
        return (False, None)

    # Equal coefficients for x^2 and y^2
    if sp.simplify(A_e - C_e) != 0:
        return (False, None)

    # Normalize so x^2 + y^2 + ... = 0
    if sp.simplify(A_e) != 1:
        Dn = sp.simplify(D_e / A_e)
        En = sp.simplify(E_e / A_e)
        Fn = sp.simplify(F_e / A_e)
    else:
        Dn, En, Fn = D_e, E_e, F_e

    return (True, (cast(Expr, Dn), cast(Expr, En), cast(Expr, Fn)))


def general_to_center_radius_rational(D: Any, E: Any, F: Any) -> Tuple[Expr, Expr, Expr, Expr]:
    """
    Convert general circle form:
        x^2 + y^2 + D x + E y + F = 0
    to (h, k, r, r2) exactly.
    """
    D_e, E_e, F_e = map(_to_expr, (D, E, F))
    h = sp.simplify(-D_e / 2)
    k = sp.simplify(-E_e / 2)
    r2 = sp.simplify(h*h + k*k - F_e)
    r = cast(Expr, sp.sqrt(r2))
    return (cast(Expr, h), cast(Expr, k), cast(Expr, r), cast(Expr, r2))


def center_radius_to_general_rational(center: Sequence[Any], radius: Any) -> Tuple[Expr, Expr, Expr]:
    """
    Convert (h,k), r to (D,E,F) for:
        x^2 + y^2 + D x + E y + F = 0
    """
    h, k = map(_to_expr, center)
    r = _to_expr(radius)
    D = sp.simplify(-2*h)
    E = sp.simplify(-2*k)
    F = sp.simplify(h*h + k*k - r*r)
    return (cast(Expr, D), cast(Expr, E), cast(Expr, F))


def standard_expr0_from_center_radius(center: Sequence[Any], radius: Any) -> Expr:
    """
    Return expression == 0 for standard form:
        (x - h)^2 + (y - k)^2 - r^2
    """
    h, k = map(_to_expr, center)
    r = _to_expr(radius)
    expr0 = sp.simplify((x - h)**2 + (y - k)**2 - r*r)
    return cast(Expr, expr0)


def circle_from_center_point_rational(center: Sequence[Any], point: Sequence[Any]) -> Tuple[Expr, Expr, Expr, Expr]:
    """Given center (h,k) and point on circle, return (h,k,r,r2) exactly."""
    h, k = map(_to_expr, center)
    x1, y1 = map(_to_expr, point)
    r2 = sp.simplify((x1 - h)**2 + (y1 - k)**2)
    r = cast(Expr, sp.sqrt(r2))
    return (cast(Expr, h), cast(Expr, k), cast(Expr, r), cast(Expr, r2))


def distance_rational(p1: Sequence[Any], p2: Sequence[Any]) -> Expr:
    """Exact Euclidean distance between two points."""
    x1, y1 = map(_to_expr, p1)
    x2, y2 = map(_to_expr, p2)
    return cast(Expr, sp.sqrt((x2 - x1)**2 + (y2 - y1)**2))


def point_circle_position_rational(center: Sequence[Any], radius: Any, point: Sequence[Any]) -> int:
    """
    Inside/on/outside test for a point relative to a circle.

    Returns:
      -1 if inside, 0 if on, +1 if outside

    Note: For symbolic inputs where the sign can't be determined, raises ValueError.
    """
    d = sp.simplify(distance_rational(center, point))
    r = sp.simplify(_to_expr(radius))
    return _sign_known(cast(Expr, d - r))


# ---------------------------------------------------------------------
# Circle construction from 3 points (exact)
# ---------------------------------------------------------------------

def circle_from_3_points_rational(
    p1: Sequence[Any], p2: Sequence[Any], p3: Sequence[Any]
) -> Dict[str, Any]:
    """
    Exact circle through 3 points (raises if collinear).

    Returns dict with:
      center: (h,k)
      radius: r
      radius_sq: r2
      D,E,F: coefficients
      general_eq: expanded expression for x^2 + y^2 + D x + E y + F
      standard_tuple: (h,k,r2)  (preserves standard structure)
      standard_str: pretty printed standard form
      standard_expr0: expression == 0 for standard form (NOT expanded)
    """
    x1, y1 = map(_to_rational_expr, p1)
    x2, y2 = map(_to_rational_expr, p2)
    x3, y3 = map(_to_rational_expr, p3)

    D, E, F = sp.symbols("D E F")

    eqs = [
        x1**2 + y1**2 + D*x1 + E*y1 + F,
        x2**2 + y2**2 + D*x2 + E*y2 + F,
        x3**2 + y3**2 + D*x3 + E*y3 + F,
    ]

    sol = sp.solve(eqs, (D, E, F), dict=True)
    if not sol:
        raise ValueError("Points are collinear — no unique circle.")

    Dv = cast(Expr, sp.simplify(sol[0][D]))
    Ev = cast(Expr, sp.simplify(sol[0][E]))
    Fv = cast(Expr, sp.simplify(sol[0][F]))

    h, k, r, r2 = general_to_center_radius_rational(Dv, Ev, Fv)

    general_eq = sp.expand(x**2 + y**2 + Dv*x + Ev*y + Fv)
    standard_tuple = (h, k, r2)
    standard_str = pretty_standard_circle(h, k, r2)
    standard_expr0 = standard_expr0_from_center_radius((h, k), r)

    return {
        "center": (h, k),
        "radius": r,
        "radius_sq": r2,
        "D": Dv, "E": Ev, "F": Fv,
        "general_eq": cast(Expr, general_eq),
        "standard_tuple": standard_tuple,
        "standard_str": standard_str,
        "standard_expr0": standard_expr0,
    }


# ---------------------------------------------------------------------
# Line-circle intersection (exact when possible)
# ---------------------------------------------------------------------

def line_circle_intersection_rational(
    m: Any, b: Any, center: Sequence[Any], radius: Any
) -> List[Tuple[Expr, Expr]]:
    """
    Intersections of y = m x + b with circle (h,k,r).

    Returns 0, 1, or 2 points, exact when inputs are exact.
    Robust for numeric and many symbolic m,b (within SymPy's abilities).
    """
    m_e, b_e = map(_to_expr, (m, b))
    h, k = map(_to_expr, center)
    r = _to_expr(radius)

    y_sub = m_e*x + b_e
    poly = sp.expand((x - h)**2 + (y_sub - k)**2 - r*r)

    xs = sp.solve(sp.Eq(poly, 0), x)

    pts: List[Tuple[Expr, Expr]] = []
    for xv in xs:
        xv_e = cast(Expr, sp.simplify(_to_expr(xv)))
        yv_e = cast(Expr, sp.simplify(m_e*xv_e + b_e))
        pts.append((xv_e, yv_e))

    # Deduplicate
    uniq: List[Tuple[Expr, Expr]] = []
    for p in pts:
        if p not in uniq:
            uniq.append(p)
    return uniq
