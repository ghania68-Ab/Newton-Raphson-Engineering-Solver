"""
main.py

Single entry point that runs both applications, saves their iteration
tables as CSV, prints a comparison summary, and generates the convergence
graph. Run this one file to reproduce every result in your report.

Usage example:
    python src/main.py
"""

import pandas as pd
from collections.abc import Callable

from application_beam import run_beam_application
from application_spring import run_spring_application
from visualization import plot_convergence
from utilities import save_table_to_csv, print_comparison_table


def run_application_safely(
    name: str,
    application_function: Callable[[], tuple[float | None, pd.DataFrame, str]],
) -> tuple[float | None, pd.DataFrame, str]:
    """Runs one application and returns an empty result if it fails."""
    try:
        return application_function()
    except Exception as error:
        print(f"Error while running {name}: {error}")
        print("Continuing with the remaining application.\n")
        return None, pd.DataFrame(), f"Failed: {error}"


def main() -> None:
    print("Running Newton-Raphson engineering applications...\n")

    beam_root, beam_table, _ = run_application_safely("Beam Deflection", run_beam_application)
    print()
    spring_root, spring_table, _ = run_application_safely("Spring Equilibrium", run_spring_application)

    if not beam_table.empty:
        save_table_to_csv(beam_table, "beam_deflection_iterations.csv")
    if not spring_table.empty:
        save_table_to_csv(spring_table, "spring_equilibrium_iterations.csv")

    results = {
        "Beam Deflection": (beam_root, beam_table),
        "Spring Equilibrium": (spring_root, spring_table),
    }
    print_comparison_table(results)

    plot_results = {
        name: (root, table, None)
        for name, (root, table) in results.items()
        if not table.empty
    }
    if plot_results:
        plot_convergence(plot_results)
    else:
        print("\nNo convergence graph was created because no application produced iteration data.")


if __name__ == "__main__":
    main()
