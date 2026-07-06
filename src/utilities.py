"""
utilities.py

Small reusable helper functions shared across the project:
- saving iteration tables to CSV
- validating an equation string before it's passed to the solver
- printing a clean comparison summary across multiple applications
"""

import os
import sympy as sp
import pandas as pd


def save_table_to_csv(table: pd.DataFrame, filename: str, folder: str = "results/iteration_tables") -> str:
    """Saves an iteration table (DataFrame) to a CSV file, creating the folder if needed."""
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    table.to_csv(filepath, index=False)
    print(f"Saved: {filepath}")
    return filepath


def validate_equation(equation_str: str) -> sp.Expr:
    """
    Checks that an equation string is valid and uses only the symbol 'x'.
    Raises a clear error instead of a confusing SymPy traceback.
    """
    x = sp.symbols('x')
    try:
        expr = sp.sympify(equation_str)
    except (sp.SympifyError, SyntaxError):
        raise ValueError(f"'{equation_str}' is not a valid mathematical expression.")

    other_symbols = expr.free_symbols - {x}
    if other_symbols:
        raise ValueError(
            f"Equation contains unknown symbol(s) {other_symbols}. "
            f"Only 'x' is allowed -- substitute all other constants with numbers first."
        )
    return expr


def print_comparison_table(results_dict: dict[str, tuple[float | None, pd.DataFrame]]) -> None:
    """
    Prints a clean comparison summary for any number of applications.

    results_dict format:
        { "Beam (Point Load)": (root, history_df), "Spring": (root, history_df), ... }
    """
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)

    names = list(results_dict.keys())
    print(f"{'Metric':<26}" + "".join(f"{name:<22}" for name in names))

    iterations_row = f"{'Iterations to converge':<26}"
    root_row = f"{'Final root':<26}"
    error_row = f"{'Final error':<26}"

    for name in names:
        root, table = results_dict[name]
        iterations_row += f"{len(table):<22}"
        root_row += f"{root:<22.5f}" if root is not None else f"{'N/A':<22}"
        error_row += f"{table['Raw Error'].iloc[-1]:<22.2e}" if not table.empty else f"{'N/A':<22}"

    print(iterations_row)
    print(root_row)
    print(error_row)