# ============================================================
# mean_value_tools.py
# Tools for Rolle's Theorem, MVT, Cauchy MVT, Higher MVT,
# and monotonicity tests.
# Using SymPy
# ============================================================

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.symbols('x', real=True)


# ------------------------------------------------------------
# 1. Rolle's Theorem: find c where f'(c) = 0 if f(a)=f(b)
# ------------------------------------------------------------
def rolles_theorem(f, a, b):
    if f.subs(x, a) != f.subs(x, b):
        return "Rolle's theorem does not apply (f(a) ≠ f(b))"

    fprime = sp.diff(f, x)
    sol = sp.solve(sp.Eq(fprime, 0), x)
    sol_in_interval = [float(s) for s in sol if s > a and s < b]

    return sol_in_interval


# ------------------------------------------------------------
# 2. Mean Value Theorem: f(b) - f(a) = f'(c)(b - a)
# ------------------------------------------------------------
def mean_value_theorem(f, a, b):
    fprime = sp.diff(f, x)
    slope_secant = (f.subs(x, b) - f.subs(x, a)) / (b - a)
    eq = sp.Eq(fprime, slope_secant)

    sol = sp.solve(eq, x)
    sol_in_interval = [float(s) for s in sol if s > a and s < b]

    return float(slope_secant), sol_in_interval


# ------------------------------------------------------------
# 3. Extended MVT (Cauchy’s Mean Value Theorem)
# Find c such that f'(c)/g'(c) = (f(b)-f(a)) / (g(b)-g(a))
# ------------------------------------------------------------
def cauchy_mvt(f, g, a, b):
    fprime = sp.diff(f, x)
    gprime = sp.diff(g, x)

    rhs = (f.subs(x, b) - f.subs(x, a)) / (g.subs(x, b) - g.subs(x, a))

    eq = sp.Eq(fprime / gprime, rhs)
    sol = sp.solve(eq, x)
    sol_in_interval = [float(s) for s in sol if s > a and s < b]

    return float(rhs), sol_in_interval


# ------------------------------------------------------------
# 4. Higher Mean Value Theorem (simple version)
# Find c such that f^(n)(c) = 0, assuming f(a)=f(b)=... up to n-th
# ------------------------------------------------------------
def higher_mvt(f, a, b, n=2):
    """
    n = 2 → f(a)=f(b)=0 guarantees a c where f''(c)=0.
    """
    fn = sp.diff(f, x, n)
    sol = sp.solve(sp.Eq(fn, 0), x)
    sol_in_interval = [float(s) for s in sol if s > a and s < b]

    return sol_in_interval


# ------------------------------------------------------------
# 5. Increasing & Decreasing functions via f′
# ------------------------------------------------------------
def monotonic_intervals(f):
    fprime = sp.diff(f, x)
    crit = sp.solve(sp.Eq(fprime, 0), x)
    crit = sorted([float(c) for c in crit])

    # Test points: midpoint between critical points
    intervals = []
    test_points = []

    # Build test points
    pts = [-10] + crit + [10]  # wide range; adjust if needed
    for i in range(len(pts) - 1):
        mid = (pts[i] + pts[i+1]) / 2
        test_points.append(mid)

    for tp in test_points:
        val = fprime.subs(x, tp)
        if val > 0:
            intervals.append(("increasing", tp))
        elif val < 0:
            intervals.append(("decreasing", tp))
        else:
            intervals.append(("flat", tp))

    return crit, intervals


# ------------------------------------------------------------
# 6. Plot secant line vs tangent line for MVT visualization
# ------------------------------------------------------------
def plot_mvt(f, a, b, c_point=None, x_range=None, num=400):
    if x_range is None:
        x_range = (a - 1, b + 1)

    f_np = sp.lambdify(x, f, "numpy")
    xs = np.linspace(x_range[0], x_range[1], num)

    # Secant line
    slope = float((f.subs(x, b) - f.subs(x, a)) / (b - a))
    y_a = float(f.subs(x, a))
    secant_np = lambda t: y_a + slope*(t - a)

    plt.figure(figsize=(8,6))
    plt.plot(xs, f_np(xs), label="f(x)", linewidth=2)
    plt.plot(xs, secant_np(xs), '--', label="Secant line AB")

    # If c is known, plot tangent line at c
    if c_point is not None:
        fprime = sp.diff(f, x)
        m_c = float(fprime.subs(x, c_point))
        y_c = float(f.subs(x, c_point))
        tangent = lambda t: y_c + m_c*(t - c_point)
        plt.plot(xs, tangent(xs), ':', label=f"Tangent at c={c_point}")
        plt.scatter([c_point], [y_c], color='red')

    plt.scatter([a, b], [float(f.subs(x,a)), float(f.subs(x,b))], color='black', label="A, B")

    plt.title("Mean Value Theorem Visualization")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    plt.show()
