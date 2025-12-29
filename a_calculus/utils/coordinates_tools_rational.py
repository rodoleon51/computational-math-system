from sympy import Rational, sqrt, Symbol, simplify
from sympy.core.numbers import Number
from sympy.core.expr import Expr
from sympy import sympify

# ---------------------------------------------------------
# Symbolic conversion helpers
# ---------------------------------------------------------
from sympy import sympify, simplify

def _to_sympy_number(x):
    """
    Convert any numeric input (int, float, Rational, Expr) into a SymPy expression.
    Ensures simplify() always receives a SymPy Basic object.
    """
    # Already a SymPy object
    if isinstance(x, (Expr, Number)):
        return x

    # Convert Python ints/floats to SymPy
    try:
        return sympify(x)
    except Exception:
        raise TypeError("Value must be numeric or a SymPy expression.")


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
    m = _to_sympy_number(m)
    x_value = _to_sympy_number(x_value)

    expr = sympify(y0 + m * (x_value - x0))
    return simplify(expr)


# ---------------------------------------------------------
# Symbolic slope-intercept evaluation
# ---------------------------------------------------------


def slope_intercept(m, b, x_value):
    m = _to_sympy_number(m)
    b = _to_sympy_number(b)
    x_value = _to_sympy_number(x_value)

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
