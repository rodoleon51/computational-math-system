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

from dataclasses import dataclass
from typing import Any, List, Sequence, Tuple, Union, Optional, cast

import sympy as sp
from sympy.core.relational import Relational
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


def _as_expr_zero(eq_or_expr: Any) -> Expr:
    """
    Normalize input into an expression `expr` meaning `expr == 0`.

    Accepts:
      - Relational (Eq/Equality/etc): returns lhs - rhs
      - Expression: returns as-is

    This helper is intentionally type-checker friendly: it `sympify()`s first and
    casts lhs/rhs to Expr before subtraction to avoid static-analysis complaints.
    """
    obj = sp.sympify(eq_or_expr)

    if isinstance(obj, Relational):
        lhs = cast(Expr, obj.lhs)
        rhs = cast(Expr, obj.rhs)
        expr = sp.simplify(lhs - rhs)
    else:
        expr = sp.simplify(obj)

    if not isinstance(expr, Expr):
        raise ValueError(f"Input could not be converted to an algebraic expression: {expr}")

    return cast(Expr, sp.expand(expr))


# ---------------------------------------------------------------------
# Extract (D,E,F) from general circle equation
# ---------------------------------------------------------------------

def extract_general_coeffs_rational(eq_or_expr: Any, x: sp.Symbol = None, y: sp.Symbol = None):
    """
    Extract (D, E, F) from a general circle equation:
        x^2 + y^2 + D*x + E*y + F = 0

    Accepts:
      - any SymPy Relational (Eq(lhs, rhs), Equality, etc.)
      - expression assumed equal to 0 if not Relational
      - list/tuple of equations/expressions (returns list of tuples)

    Returns:
      (D, E, F) as exact SymPy expressions (Rational/Expr)

    Raises:
      ValueError if the expression is not exactly in the allowed general form.
    """
    # Allow batch input
    if isinstance(eq_or_expr, (list, tuple)):
        return [extract_general_coeffs_rational(item, x=x, y=y) for item in eq_or_expr]

    # Symbols
    if x is None:
        x = sp.Symbol("x")
    if y is None:
        y = sp.Symbol("y")

    expr = _as_expr_zero(eq_or_expr)

    # Try polynomial extraction first (catches x*y, x**2 terms, etc.)
    poly = None
    try:
        poly = sp.Poly(expr, x, y, domain="EX")
    except Exception:
        poly = None

    if poly is not None:
        # Required quadratic terms
        if sp.simplify(poly.coeff_monomial(x**2) - 1) != 0 or sp.simplify(poly.coeff_monomial(y**2) - 1) != 0:
            raise ValueError(
                "Not in circle general form: expected x^2 and y^2 with coefficient 1. "
                f"Got: {expr}"
            )

        # Disallow other degree-2 terms (like x*y)
        if sp.simplify(poly.coeff_monomial(x * y)) != 0:
            raise ValueError(
                f"Not in circle general form: cross-term x*y present. Got: {expr}"
            )

        D = sp.simplify(poly.coeff_monomial(x))
        E = sp.simplify(poly.coeff_monomial(y))
        F = sp.simplify(poly.coeff_monomial(1))

        # Ensure no other polynomial terms remain (e.g., x**3, y**4, etc.)
        residual = sp.simplify(expr - (x**2 + y**2 + D * x + E * y + F))
        if residual != 0:
            raise ValueError(
                f"Expression has extra terms beyond x^2+y^2+Dx+Ey+F: {residual}"
            )

        return (cast(Expr, D), cast(Expr, E), cast(Expr, F))

    # Fallback for non-polynomial expressions (e.g., contains sqrt, trig, etc.)
    # Extract linear-looking coefficients, then validate by residual check.
    D = sp.simplify(expr.coeff(x, 1).subs(y, 0))
    E = sp.simplify(expr.coeff(y, 1).subs(x, 0))
    F = sp.simplify((expr - x**2 - y**2 - D * x - E * y).subs({x: 0, y: 0}))

    residual = sp.simplify(expr - (x**2 + y**2 + D * x + E * y + F))
    if residual != 0:
        raise ValueError(
            "Not in general circle form x^2+y^2+Dx+Ey+F=0. "
            f"Extra/nonlinear terms detected: {residual}"
        )

    return (cast(Expr, D), cast(Expr, E), cast(Expr, F))


def extract_general_coeffs_rational_safe_batch(equations: Sequence[Any], x: sp.Symbol = None, y: sp.Symbol = None):
    """
    Safe batch wrapper around extract_general_coeffs_rational(...).

    Returns a list of dicts, one per input item:
      {
        "ok": True/False,
        "input": original_item,
        "D": D, "E": E, "F": F,          # only if ok
        "coeffs": (D,E,F),              # only if ok
        "error": "message",             # only if not ok
      }
    """
    results: List[dict] = []
    for item in equations:
        try:
            D, E, F = extract_general_coeffs_rational(item, x=x, y=y)
            results.append(
                {
                    "ok": True,
                    "input": item,
                    "D": D,
                    "E": E,
                    "F": F,
                    "coeffs": (D, E, F),
                }
            )
        except Exception as e:
            results.append(
                {
                    "ok": False,
                    "input": item,
                    "error": f"{type(e).__name__}: {e}",
                }
            )
    return results


def apply_general_to_center_radius_safe_batch(equations: Sequence[Any], x: sp.Symbol = None, y: sp.Symbol = None):
    """
    One-shot safe batch (no extra args needed):
      equations -> (D,E,F) extraction -> general_to_center_radius_rational(D,E,F)

    Returns list of dicts:
      {
        "ok": True/False,
        "input": original_item,
        "D":..., "E":..., "F":...,                 # if extracted
        "center_radius": (h,k,r,r2),               # if ok
        "error": "message",                        # if not ok
        "stage": "extract" or "convert"            # where it failed
      }
    """
    out: List[dict] = []
    for item in equations:
        try:
            D, E, F = extract_general_coeffs_rational(item, x=x, y=y)
        except Exception as e:
            out.append(
                {
                    "ok": False,
                    "stage": "extract",
                    "input": item,
                    "error": f"{type(e).__name__}: {e}",
                }
            )
            continue

        try:
            cr = general_to_center_radius_rational(D, E, F)
            out.append(
                {
                    "ok": True,
                    "input": item,
                    "D": D,
                    "E": E,
                    "F": F,
                    "center_radius": cr,
                }
            )
        except Exception as e:
            out.append(
                {
                    "ok": False,
                    "stage": "convert",
                    "input": item,
                    "D": D,
                    "E": E,
                    "F": F,
                    "error": f"{type(e).__name__}: {e}",
                }
            )
    return out


# ---------------------------------------------------------------------
# Pretty printing
# ---------------------------------------------------------------------

def _fmt_shift(var: str, a: Expr) -> str:
    """Format 'x - a' with clean signs: x, x - 3, x + 3, x - 5/2, ..."""
    a = sp.simplify(_to_expr(a))
    if a == 0:
        return var
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
    r2 = sp.simplify(h * h + k * k - F_e)
    r = cast(Expr, sp.sqrt(r2))
    return (cast(Expr, h), cast(Expr, k), cast(Expr, r), cast(Expr, r2))


def center_radius_to_general_rational(center: Sequence[Any], radius: Any) -> Tuple[Expr, Expr, Expr]:
    """
    Convert (h,k), r to (D,E,F) for:
        x^2 + y^2 + D x + E y + F = 0
    """
    h, k = map(_to_rational_expr, center)
    r = _to_rational_expr(radius)
    D = sp.simplify(-2 * h)
    E = sp.simplify(-2 * k)
    F = sp.simplify(h * h + k * k - r * r)
    return (cast(Expr, D), cast(Expr, E), cast(Expr, F))


def standard_expr0_from_center_radius(center: Sequence[Any], radius: Any) -> Expr:
    """
    Return expression == 0 for standard form:
        (x - h)^2 + (y - k)^2 - r^2
    """
    h, k = map(_to_expr, center)
    r = _to_expr(radius)
    expr0 = sp.simplify((x - h) ** 2 + (y - k) ** 2 - r * r)
    return cast(Expr, expr0)


def circle_from_center_point_rational(center: Sequence[Any], point: Sequence[Any]) -> Tuple[Expr, Expr, Expr, Expr]:
    """Given center (h,k) and point on circle, return (h,k,r,r2) exactly."""
    h, k = map(_to_expr, center)
    x1, y1 = map(_to_expr, point)
    r2 = sp.simplify((x1 - h) ** 2 + (y1 - k) ** 2)
    r = cast(Expr, sp.sqrt(r2))
    return (cast(Expr, h), cast(Expr, k), cast(Expr, r), cast(Expr, r2))


def distance_rational(p1: Sequence[Any], p2: Sequence[Any]) -> Expr:
    """Exact Euclidean distance between two points."""
    x1, y1 = map(_to_expr, p1)
    x2, y2 = map(_to_expr, p2)
    return cast(Expr, sp.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


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
) -> dict:
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
    """
    x1, y1 = map(_to_rational_expr, p1)
    x2, y2 = map(_to_rational_expr, p2)
    x3, y3 = map(_to_rational_expr, p3)

    D, E, F = sp.symbols("D E F")

    eqs = [
        x1 ** 2 + y1 ** 2 + D * x1 + E * y1 + F,
        x2 ** 2 + y2 ** 2 + D * x2 + E * y2 + F,
        x3 ** 2 + y3 ** 2 + D * x3 + E * y3 + F,
    ]

    sol = sp.solve(eqs, (D, E, F), dict=True)
    if not sol:
        raise ValueError("Points are collinear — no unique circle.")

    Dv = cast(Expr, sp.simplify(sol[0][D]))
    Ev = cast(Expr, sp.simplify(sol[0][E]))
    Fv = cast(Expr, sp.simplify(sol[0][F]))

    h, k, r, r2 = general_to_center_radius_rational(Dv, Ev, Fv)

    general_eq = sp.expand(x ** 2 + y ** 2 + Dv * x + Ev * y + Fv)
    standard_tuple = (h, k, r, r2)
    standard_str = pretty_standard_circle(h, k, r2)

    return {
        "center": (h, k),
        "radius": r,
        "radius_sq": r2,
        "D": Dv,
        "E": Ev,
        "F": Fv,
        "general_eq": cast(Expr, general_eq),
        "standard_tuple": standard_tuple,
        "standard_str": standard_str,
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

    y_sub = m_e * x + b_e
    poly = sp.expand((x - h) ** 2 + (y_sub - k) ** 2 - r * r)

    xs = sp.solve(sp.Eq(poly, 0), x)

    pts: List[Tuple[Expr, Expr]] = []
    for xv in xs:
        xv_e = cast(Expr, sp.simplify(_to_expr(xv)))
        yv_e = cast(Expr, sp.simplify(m_e * xv_e + b_e))
        pts.append((xv_e, yv_e))

    # Deduplicate
    uniq: List[Tuple[Expr, Expr]] = []
    for p in pts:
        if p not in uniq:
            uniq.append(p)
    return uniq


# ---------------------------------------------------------------------
# circle_through_point_tangent_line_at_point_
# ---------------------------------------------------------------------

def circle_through_point_tangent_line_at_point_rational(
    P: Sequence[Any],
    line_ABC: Sequence[Any],  # (A, B, C) for Ax + By + C = 0
    T: Sequence[Any],
) -> dict:
    """
    Circle that passes through point P and is tangent to line Ax + By + C = 0
    at point T.

    Geometry:
      - Radius at T is perpendicular to the tangent line
      - Center lies on the normal through T

    Returns dict with:
      center, radius, radius_sq,
      general_eq,
      standard_tuple, standard_str, standard_expr0
    """
    Px, Py = map(_to_expr, P)
    Tx, Ty = map(_to_expr, T)
    A, B, C = map(_to_expr, line_ABC)

    # Validate tangency point
    if sp.simplify(A * Tx + B * Ty + C) != 0:
        raise ValueError("Point T must lie on the line Ax + By + C = 0.")

    dx = Tx - Px
    dy = Ty - Py

    denom = sp.simplify(A * dx + B * dy)
    num = sp.simplify(dx * dx + dy * dy)

    if denom == 0:
        if num == 0:
            raise ValueError("P coincides with T: infinitely many tangent circles.")
        raise ValueError("No solution: PT is perpendicular to the line normal.")

    # Parameter along the normal direction
    t = sp.simplify(-num / (2 * denom))

    # Center
    h = sp.simplify(Tx + t * A)
    k = sp.simplify(Ty + t * B)

    # Radius
    r2 = sp.simplify((h - Tx) ** 2 + (k - Ty) ** 2)
    r = sp.sqrt(r2)

    # General form
    D = sp.simplify(-2 * h)
    E = sp.simplify(-2 * k)
    F = sp.simplify(h * h + k * k - r2)
    general_eq = sp.expand(x ** 2 + y ** 2 + D * x + E * y + F)

    # Standard representations
    standard_tuple = (h, k, r2)
    standard_str = pretty_standard_circle(h, k, r2)
    standard_expr0 = standard_expr0_from_center_radius((h, k), r)

    return {
        "center": (h, k),
        "radius": r,
        "radius_sq": r2,
        "D": D,
        "E": E,
        "F": F,
        "general_eq": general_eq,
        "standard_tuple": standard_tuple,
        "standard_str": standard_str,
        "standard_expr0": standard_expr0,
        "t": t,  # useful for teaching/debugging
    }
