# tangent_tools.py
import sympy as sp
from sympy import diff, solve, Eq, oo
import matplotlib.pyplot as plt
import numpy as np

x, y, t, theta = sp.symbols('x y t theta')

def tangent_normal(
    f=None, x0=None, y0=None,
    parametric=None, polar=None,
    implicit=None, var='x',
    show_plot=True, point_size=50
):
    """
    Universal tangent & normal line calculator.
    Call with exactly one of: f, parametric, polar, or implicit.
    """
    result = {}

    if f is not None:  # Explicit: y = f(x)
        if x0 is None or y0 is None:
            raise ValueError("For explicit functions, provide x0 and y0")
        
        dy_dx = diff(f, x)
        m = dy_dx.subs(x, x0)
        m = m.doit() if hasattr(m, 'doit') else m

        y0_val = f.subs(x, x0)

        tangent_eq = y - y0_val - m * (x - x0)
        if m == 0:
            normal_eq = x - x0
        elif m is oo or abs(m) > 1e10:
            normal_eq = y - y0_val
        else:
            normal_eq = y - y0_val + (1/m) * (x - x0)

        result = {
            'type': 'explicit',
            'point': (float(x0), float(y0_val)),
            'slope': m if m != oo else '∞ (vertical)',
            'tangent': Eq(y, m*(x - x0) + y0_val),
            'normal': Eq(y, (-1/m)*(x - x0) + y0_val) if m not in [0, oo] else normal_eq,
            'dy_dx': dy_dx
        }

    elif parametric is not None:  # Parametric: (x(t), y(t))
        xt, yt = parametric
        if y0 is not None and x0 is None:
            t0 = y0  # user passed t0 as second argument
        else:
            t0 = solve(xt - x0, t)[0] if x0 is not None else y0

        dxdt = diff(xt, t)
        dydt = diff(yt, t)
        dydx = sp.simplify(dydt / dxdt)
        m = dydx.subs(t, t0)

        x0_val = xt.subs(t, t0)
        y0_val = yt.subs(t, t0)

        tangent_eq = Eq(y - y0_val, m * (x - x0_val))
        normal_slope = -1/m if m not in [0, oo] else None

        result = {
            'type': 'parametric',
            't0': t0,
            'point': (x0_val, y0_val),
            'slope': m,
            'tangent': tangent_eq,
            'normal': Eq(y - y0_val, normal_slope * (x - x0_val)) if normal_slope else Eq(x, x0_val)
        }

    elif polar is not None:  # Polar: r(θ)
        r = polar
        x_pol = r * sp.cos(theta)
        y_pol = r * sp.sin(theta)

        if y0 is not None and x0 is None:
            theta0 = y0
        else:
            theta0 = solve(x_pol - x0, theta)[0]

        dxdtheta = diff(x_pol, theta)
        dydtheta = diff(y_pol, theta)
        dydx = sp.simplify(dydtheta / dxdtheta)
        m = dydx.subs(theta, theta0)

        x0_val = x_pol.subs(theta, theta0)
        y0_val = y_pol.subs(theta, theta0)

        result = {
            'type': 'polar',
            'theta0': theta0,
            'point': (x0_val, y0_val),
            'slope': m,
            'tangent': Eq(y - y0_val, m * (x - x0_val)),
            'normal': Eq(y - y0_val, -1/m * (x - x0_val)) if m != 0 else Eq(x, x0_val)
        }

    elif implicit is not None:  # Implicit: F(x,y) = 0
        if x0 is None or y0 is None:
            raise ValueError("Need x0 and y0 for implicit")
        
        Fx = diff(implicit, x)
        Fy = diff(implicit, y)
        m = -Fx.subs({x: x0, y: y0}) / Fy.subs({x: x0, y: y0})

        result = {
            'type': 'implicit',
            'point': (x0, y0),
            'slope': m,
            'tangent': Eq(y - y0, m * (x - x0)),
            'normal': Eq(y - y0, -1/m * (x - x0)) if m != 0 else Eq(x, x0)
        }

    # Print results nicely
    print(f"Tangent and Normal at point {result['point']}")
    print(f"Slope of tangent: {result['slope']}")
    print(f"Tangent line: {result['tangent']}")
    print(f"Normal line : {result['normal']}\n")

    # Optional plot
    if show_plot:
        plot_tangent_normal(result, f=f, parametric=parametric, polar=polar, implicit=implicit)

    return result


def plot_tangent_normal(res, f=None, parametric=None, polar=None, implicit=None, rang=5):
    """Helper function to plot curve + tangent + normal"""
    plt.figure(figsize=(10, 8))
    x_vals = np.linspace(res['point'][0] - rang, res['point'][0] + rang, 500)

    # Plot original curve
    if f is not None:
        y_func = sp.lambdify(x, f, 'numpy')
        plt.plot(x_vals, y_func(x_vals), label='Curve', linewidth=3, color='blue')
    elif implicit is not None:
        X, Y = np.meshgrid(np.linspace(res['point'][0]-rang, res['point'][0]+rang, 600),
                           np.linspace(res['point'][1]-rang, res['point'][1]+rang, 600))
        F = sp.lambdify((x, y), implicit, 'numpy')
        plt.contour(X, Y, F(X, Y), levels=[0], colors='blue', linewidths=3)

    # Plot tangent and normal
    tan_lamb = sp.lambdify(x, res['tangent'].rhs, 'numpy')
    plt.plot(x_vals, tan_lamb(x_vals), '--', label='Tangent', color='green', linewidth=2)

    try:
        nor_lamb = sp.lambdify(x, res['normal'].rhs, 'numpy')
        plt.plot(x_vals, nor_lamb(x_vals), '--', label='Normal', color='red', linewidth=2)
    except:
        pass  # vertical normal

    plt.scatter(*res['point'], color='black', s=80, zorder=5)
    plt.axhline(0, color='k', linewidth=0.5); plt.axvline(0, color='k', linewidth=0.5)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title(f"Tangent (green) and Normal (red) at {res['point']}")
    plt.xlabel('x'); plt.ylabel('y')
    plt.axis('equal')
    plt.show()