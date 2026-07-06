"""
application_beam.py

Engineering Application 1: Beam Deflection Position Analysis

A simply supported beam under a concentrated point load at its center has a
deflection at position x along its span given by:

    delta(x) = P*x*(3*L^2 - 4*x^2) / (48*E*I),   valid for 0 <= x <= L/2

Setting delta(x) - delta_target = 0 and simplifying gives a cubic equation
in x -- power-rule derivative only.
"""

import pandas as pd

from newton_raphson import newton_raphson


def run_beam_application(x0: float = 1.0, tol: float = 1e-6, verbose: bool = True) -> tuple[float | None, pd.DataFrame, str]:
    """
    Sets up and solves the beam deflection problem.
    Returns (root, history_table, status_message).
    """
    # ---- Beam parameters (edit these to match your own example) ----
    L = 6.0                 # beam span (m)
    P = 15000.0              # concentrated point load at center (N)
    E = 200e9                # Young's modulus -- steel (Pa)
    I = 2e-5                 # moment of inertia (m^4)
    delta_target = 0.005     # allowable deflection (m) = 5 mm

    # Build the equation string with the numbers plugged in
    const_term = (48.0 * E * I * delta_target) / P
    equation_str = f"4*x**3 - {3.0 * L**2}*x + {const_term}"
    valid_range = (0, L / 2)

    if verbose:
        print("=" * 65)
        print("APPLICATION 1: BEAM DEFLECTION PROBLEM (Concentrated Point Load)")
        print("=" * 65)
        print(f"Beam span (L)        : {L} m")
        print(f"Point load (P)       : {P} N")
        print(f"Young's modulus (E)  : {E:.2e} Pa")
        print(f"Moment of inertia (I): {I:.1e} m^4")
        print(f"Allowable deflection : {delta_target} m\n")

    result = newton_raphson(equation_str, x0=x0, tol=tol)
    root, table, status = result["root"], result["history"], result["status"]

    if verbose:
        print(table.to_string(index=False))
        print(f"\n{status}")
        if root is not None:
            print(f"Root found at x = {root:.5f} m")
            low, high = valid_range
            if low <= root <= high:
                print(f"Valid: this lies within the beam's physical domain [{low}, {high}] m.")
            else:
                print(f"Warning: this lies outside the physical domain [{low}, {high}] m.")

    return root, table, status


if __name__ == "__main__":
    run_beam_application(x0=1.0)
