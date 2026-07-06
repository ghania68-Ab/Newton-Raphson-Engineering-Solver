"""
application_spring.py

Engineering Application 2: Nonlinear Spring-Mass Equilibrium

A spring with a nonlinear cubic stiffening term:
    F(x) = k*x + beta*x^3

At equilibrium the spring force balances the applied load:
    k*x + beta*x^3 - F_applied = 0

This is a cubic polynomial equation in x -- power-rule derivative only.
"""

import pandas as pd

from newton_raphson import newton_raphson


def run_spring_application(x0: float = 2.0, tol: float = 1e-6, verbose: bool = True) -> tuple[float | None, pd.DataFrame, str]:
    """
    Sets up and solves the nonlinear spring-mass equilibrium problem.
    Returns (root, history_table, status_message).
    """
    k = 500.0           # linear spring constant (N/m)
    beta = 50.0         # nonlinear stiffening coefficient (N/m^3)
    F_applied = 2000.0  # applied force (N)

    equation_str = f"{k}*x + {beta}*x**3 - {F_applied}"

    if verbose:
        print("=" * 65)
        print("APPLICATION 2: NONLINEAR SPRING-MASS EQUILIBRIUM")
        print("=" * 65)
        print(f"Linear spring constant (k)      : {k} N/m")
        print(f"Nonlinear stiffening term (beta): {beta} N/m^3")
        print(f"Applied force                   : {F_applied} N\n")

    result = newton_raphson(equation_str, x0=x0, tol=tol)
    root, table, status = result["root"], result["history"], result["status"]

    if verbose:
        print(table.to_string(index=False))
        print(f"\n{status}")
        if root is not None:
            print(f"Equilibrium displacement: x = {root:.5f} m")
            linear_only = F_applied / k
            print(f"(A purely linear spring would predict x = {linear_only:.5f} m --")
            print(f" the {((linear_only - root) / linear_only) * 100:.1f}% difference shows the effect of the nonlinear term.)")

    return root, table, status


if __name__ == "__main__":
    run_spring_application()
