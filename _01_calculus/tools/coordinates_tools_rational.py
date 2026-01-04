from sympy import Rational, sqrt, Symbol, simplify
from sympy.core.numbers import Number
from sympy.core.expr import Expr
from sympy import sympify

# ---------------------------------------------------------
# Symbolic conversion helpers
# ---------------------------------------------------------
from sympy import sympify, simplify


def _to_sympy_number(x, allow_symbol: bool = False, allowed_symbols=None):
    """
    Convert input to a SymPy numeric expression.

    - Accepts Python numeric types (int, float) and SymPy numeric types (Rational, Number).
    - For strings or SymPy expressions containing symbols, allow only when allow_symbol=True
      and any present symbols are within allowed_symbols (if provided).
    - Reject non-numeric symbolic values when allow_symbol=False.
    """
    # Normalize allowed symbol names (compare by string repr to avoid .name typing issues)
    allowed_names = None
    if allowed_symbols is not None:
        allowed_names = set(str(s) for s in allowed_symbols)

    # If it's already a SymPy object
    if isinstance(x, (Expr, Number)):
        # SymPy numeric types (Number) are always allowed
        if isinstance(x, Number):
            return x
        # For general expressions, check if they contain symbols
        if hasattr(x, "free_symbols") and x.free_symbols:
            if allow_symbol:
                if allowed_names is None:
                    return x
                # Ensure all free symbols are allowed (compare via str(sym))
                if all(str(sym) in allowed_names for sym in x.free_symbols):
                    return x
            raise TypeError("Value must be numeric, not symbolic.")
        return x

    # Try converting via sympify (handles ints, floats, numeric strings, etc.)
    try:
        val = sympify(x)
    except Exception:
        raise TypeError("Value must be numeric or a SymPy expression.")

    # If conversion yields a symbolic expression, allow only when requested
    if isinstance(val, Expr) and not isinstance(val, Number):
        if hasattr(val, "free_symbols") and val.free_symbols:
            if allow_symbol:
                if allowed_names is None:
                    return val
                if all(str(sym) in allowed_names for sym in val.free_symbols):
                    return val
            raise TypeError("Value must be numeric, not symbolic.")
    return val


# ---------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------


def _validate_point(p):
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        raise TypeError("Point must be a tuple or list of length 2.")
    x, y = p
    if not isinstance(x, (int, float, Number, Expr)) or not isinstance(
        y, (int, float, Number, Expr)
    ):
        raise TypeError("Point coordinates must be numeric or SymPy expressions.")
    return (x, y)


# def _to_sympy_number(x):
#     if isinstance(x, (int, float)):
#         return Rational(x) if float(x).is_integer() else x
#     if isinstance(x, (Number, Expr)):
#         return x
#     raise TypeError("Value must be numeric or a SymPy expression.")


# ---------------------------------------------------------
# Symbolic distance
# ---------------------------------------------------------


def distance(p1, p2):
    x1, y1 = _validate_point(p1)
    x2, y2 = _validate_point(p2)

    x1, y1 = _to_sympy_number(x1), _to_sympy_number(y1)
    x2, y2 = _to_sympy_number(x2), _to_sympy_number(y2)

    return simplify(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


# ---------------------------------------------------------
# Symbolic midpoint
# ---------------------------------------------------------


def midpoint(p1, p2):
    x1, y1 = _validate_point(p1)
    x2, y2 = _validate_point(p2)

    x1, y1 = _to_sympy_number(x1), _to_sympy_number(y1)
    x2, y2 = _to_sympy_number(x2), _to_sympy_number(y2)

    return (simplify((x1 + x2) / 2), simplify((y1 + y2) / 2))


# ---------------------------------------------------------
# Symbolic slope
# ---------------------------------------------------------


def slope(p1, p2):
    x1, y1 = _validate_point(p1)
    x2, y2 = _validate_point(p2)

    x1, y1 = _to_sympy_number(x1), _to_sympy_number(y1)
    x2, y2 = _to_sympy_number(x2), _to_sympy_number(y2)

    if x1 == x2:
        raise ValueError("Slope is undefined for vertical lines.")

    return simplify((y2 - y1) / (x2 - x1))


# ---------------------------------------------------------
# Symbolic point-slope evaluation
# ---------------------------------------------------------


def point_slope(p, m, x_value):
    x0, y0 = _validate_point(p)
    m = _to_sympy_number(m, allow_symbol=False)
    x_value = _to_sympy_number(x_value, allow_symbol=True)

    expr = sympify(y0 + m * (x_value - x0))
    return simplify(expr)


# ---------------------------------------------------------
# Symbolic slope-intercept evaluation
# ---------------------------------------------------------


def slope_intercept(m, b, x_value):
    # Allow symbolic 'm' as the slope, but require numeric b and x_value
    m = _to_sympy_number(m, allow_symbol=True, allowed_symbols={"m"})
    b = _to_sympy_number(b, allow_symbol=False)
    x_value = _to_sympy_number(x_value, allow_symbol=False)

    expr = sympify(m * x_value + b)
    return simplify(expr)


# ---------------------------------------------------------
# Quadrant (same as numeric version)
# ---------------------------------------------------------


def quadrant(p):
    x, y = _validate_point(p)
    x, y = _to_sympy_number(x), _to_sympy_number(y)

    if x == 0 or y == 0:
        return 0
    if x > 0 and y > 0:
        return 1
    if x < 0 and y > 0:
        return 2
    if x < 0 and y < 0:
        return 3
    if x > 0 and y < 0:
        return 4
