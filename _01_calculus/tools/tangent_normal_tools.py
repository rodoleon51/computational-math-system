# ============================================
# tangent_normal_tools.py
# Tools for Tangents & Normals (with plotting)
# Using SymPy + Matplotlib
# ============================================

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# 1) Tangent & normal for explicit function y = f(x)
# -------------------------------------------------------------------
def tangent_normal_explicit(fx, x0):
    x = sp.symbols('x', real=True)

    fprime = sp.diff(fx, x)
    y0 = fx.subs(x, x0)
    slope = fprime.subs(x, x0)

    tangent = y0 + slope*(x - x0)

    if slope == 0:
        normal_eq = sp.Eq(x, x0)
    else:
        normal_slope = -1/slope
        normal = y0 + normal_slope*(x - x0)
        normal_eq = sp.Eq(sp.symbols('y'), normal)

    tangent_eq = sp.Eq(sp.symbols('y'), tangent)

    return {
        "y0": float(y0),
        "slope": float(slope),
        "tangent": tangent_eq,
        "normal": normal_eq
    }


# -------------------------------------------------------------------
# 2) Tangent to implicit curve F(x,y) = 0 with GIVEN slope m
# -------------------------------------------------------------------
def tangent_to_implicit_with_slope(F, m):
    x, y = sp.symbols('x y', real=True)
    Fx = sp.diff(F, x)
    Fy = sp.diff(F, y)

    dydx = -Fx / Fy

    eq1 = sp.simplify(F)
    eq2 = sp.simplify(dydx - m)

    sol = sp.solve([eq1, eq2], [x, y], dict=True)
    return sol


# -------------------------------------------------------------------
# 3) Horizontal & Vertical tangents for implicit curve
# -------------------------------------------------------------------
def horizontal_vertical_tangents(F):
    x, y = sp.symbols('x y', real=True)
    Fx = sp.diff(F, x)
    Fy = sp.diff(F, y)

    horiz = sp.solve([F, Fx], [x, y], dict=True)
    vert = sp.solve([F, Fy], [x, y], dict=True)

    return horiz, vert


# -------------------------------------------------------------------
# 4) PLOTTING — explicit function and its tangent & normal
# -------------------------------------------------------------------
def plot_explicit_tangent_normal(fx, x0, x_range=(-5, 5), num=400):
    """
    fx : SymPy expression in x
    x0 : point of tangency
    """
    x = sp.symbols('x', real=True)

    data = tangent_normal_explicit(fx, x0)

    # Convert to numeric functions
    f_np = sp.lambdify(x, fx, "numpy")

    tangent_expr = data["tangent"].rhs
    normal_expr  = data["normal"].rhs

    tan_np = sp.lambdify(x, tangent_expr, "numpy")
    nor_np = sp.lambdify(x, normal_expr, "numpy")

    # Prepare x-grid
    xs = np.linspace(x_range[0], x_range[1], num)

    plt.figure(figsize=(8,6))
    plt.plot(xs, f_np(xs), label="f(x)", linewidth=2)
    plt.plot(xs, tan_np(xs), label="Tangent line", linestyle="--")
    plt.plot(xs, nor_np(xs), label="Normal line", linestyle=":")
    plt.scatter([x0], [data["y0"]], color='red', label="Point of tangency")

    plt.title("Tangent & Normal Lines (Explicit Function)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()


# -------------------------------------------------------------------
# 5) PLOTTING — implicit curve with a tangent line at a point
# -------------------------------------------------------------------
def plot_implicit_tangent(F, point, x_range=(-10, 10), y_range=(-10, 10), num=400):
    """
    F : implicit expression F(x,y)=0
    point : tuple (x0, y0)
    """
    x, y = sp.symbols('x y', real=True)

    x0, y0 = point

    # Compute slope dy/dx at the point
    Fx = sp.diff(F, x)
    Fy = sp.diff(F, y)
    slope = float((-Fx/Fy).subs({x: x0, y: y0}))

    # Tangent line: y - y0 = m(x - x0)
    t = sp.symbols('t')
    tangent_expr = slope*(x - x0) + y0
    tan_np = sp.lambdify(x, tangent_expr, "numpy")

    # Generate grid for implicit curve
    xs = np.linspace(x_range[0], x_range[1], num)
    ys = np.linspace(y_range[0], y_range[1], num)
    XX, YY = np.meshgrid(xs, ys)

    F_np = sp.lambdify((x, y), F, "numpy")
    ZZ = F_np(XX, YY)

    plt.figure(figsize=(8,6))
    plt.contour(XX, YY, ZZ, levels=[0], colors='blue', linewidths=2, label="Curve")

    plt.plot(xs, tan_np(xs), 'r--', label="Tangent line")
    plt.scatter([x0], [y0], color='red', label="Point on curve")

    plt.title("Implicit Curve with Tangent Line")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()
