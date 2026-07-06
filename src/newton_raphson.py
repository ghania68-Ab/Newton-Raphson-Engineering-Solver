"""
newton_raphson.py

A generalized Newton-Raphson solver for nonlinear (polynomial) equations.
Uses SymPy to automatically compute the derivative, so no manual
differentiation is required.

Includes three safety checks that make the solver genuinely robust:
1. Zero-derivative check   -- stops instead of crashing if f'(x) is ~0
2. Divergence check        -- stops if the iterate blows up to infinity
3. Cycle (oscillation) check -- stops if the solver gets stuck bouncing
   between the same values forever instead of converging

These checks are simple to explain: Newton-Raphson can fail in exactly
these three ways, so we detect each one and report it clearly instead of
letting the program crash or loop forever.

Each iteration also records an empirical "Order Estimate"
(log(error_n+1) / log(error_n)), which should trend toward ~2.0 as the
solver converges -- this is the quadratic convergence Newton-Raphson is
known for.
"""

import sympy as sp
import pandas as pd
import numpy as np

from utilities import validate_equation


def newton_raphson(equation_str: str, x0: float, tol: float = 1e-6, max_iter: int = 50) -> dict:
    """
    Solve f(x) = 0 using the Newton-Raphson method.

    Parameters:
        equation_str : str   -> equation as a string, e.g. "x**3 - x - 2"
        x0           : float -> initial guess
        tol          : float -> stopping tolerance
        max_iter     : int   -> maximum number of iterations allowed

    Returns a dictionary:
        root       -> approximate root (None if it failed)
        history    -> DataFrame of every iteration
        converged  -> True/False
        status     -> plain-English message explaining what happened
    """
    x = sp.symbols('x')
    f_expr = validate_equation(equation_str)
    f_prime_expr = sp.diff(f_expr, x)      # SymPy computes this automatically

    f = sp.lambdify(x, f_expr, 'math')
    f_prime = sp.lambdify(x, f_prime_expr, 'math')

    history: list[dict[str, float | int | None]] = []
    x_current = float(x0)
    converged = False
    status_msg = "Max iterations reached without convergence."
    seen_points = []
    prev_error = None

    if tol <= 0:
        return {
            "root": None,
            "history": pd.DataFrame(history),
            "converged": False,
            "status": "Stopped: tolerance must be greater than zero.",
        }

    if max_iter <= 0:
        return {
            "root": None,
            "history": pd.DataFrame(history),
            "converged": False,
            "status": "Stopped: max_iter must be greater than zero.",
        }

    for n in range(max_iter):
        seen_points.append(x_current)

        fx = float(f(x_current))
        fpx = float(f_prime(x_current))

        # Check 1: zero derivative -- the tangent line is flat, can't proceed
        if abs(fpx) < 1e-12:
            status_msg = f"Stopped: derivative became ~0 at x = {x_current:.5f}."
            break

        x_next = float(x_current - fx / fpx)
        error = abs(x_next - x_current)

        order_estimate = None
        if prev_error is not None and prev_error > 0 and error > 0:
            order_estimate = round(np.log(error) / np.log(prev_error), 3)

        history.append({
            "Iteration": n,
            "x_n": round(x_current, 6),
            "f(x_n)": round(fx, 6),
            "f'(x_n)": round(fpx, 6),
            "x_(n+1)": round(x_next, 6),
            "Error": round(error, 6),
            "Order Estimate": order_estimate,
            "Raw Error": error,
        })
        prev_error = error

        # Check 2: divergence -- the guess is running away to infinity
        if np.isnan(x_next) or np.isinf(x_next) or abs(x_next) > 1e10:
            status_msg = f"Stopped: solution diverged after {n+1} iterations."
            break

        # Check convergence BEFORE checking for cycles. Otherwise, a solution
        # that has essentially converged (x_next almost equal to x_current)
        # would incorrectly look like a repeated/cycled value.
        if error < tol:
            x_current = x_next
            converged = True
            status_msg = f"Converged successfully in {n+1} iterations."
            break

        # Check 3: cycle detection -- guess is bouncing between old values
        # without ever getting closer to a root (exclude the current point
        # itself, since being close to yourself just means convergence).
        if any(abs(x_next - p) < 1e-9 for p in seen_points[:-1]):
            status_msg = f"Stopped: solver detected an oscillating cycle near x = {x_current:.5f}."
            break

        x_current = x_next

    return {
        "root": x_current if converged else None,
        "history": pd.DataFrame(history),
        "converged": converged,
        "status": status_msg,
    }


if __name__ == "__main__":
    # Quick test using the same equation solved by hand earlier: x^3 - x - 2 = 0
    result = newton_raphson("x**3 - x - 2", x0=1.5)
    print(result["status"])
    print(result["history"].to_string(index=False))
    print(f"\nFinal root: {result['root']:.5f}")