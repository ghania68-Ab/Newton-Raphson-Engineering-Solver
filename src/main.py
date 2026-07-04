"""
main.py

Single entry point that runs both applications, saves their iteration
tables as CSV, prints a comparison summary, and generates the convergence
graph. Run this one file to reproduce every result in your report.
"""

from application_beam import run_beam_application
from application_spring import run_spring_application
from visualization import plot_convergence
from utilities import save_table_to_csv, print_comparison_table


def main():
    print("Running Newton-Raphson engineering applications...\n")

    beam_root, beam_table, _ = run_beam_application()
    print()
    spring_root, spring_table, _ = run_spring_application()

    save_table_to_csv(beam_table, "beam_deflection_iterations.csv")
    save_table_to_csv(spring_table, "spring_equilibrium_iterations.csv")

    results = {
        "Beam Deflection": (beam_root, beam_table),
        "Spring Equilibrium": (spring_root, spring_table),
    }
    print_comparison_table(results)

    plot_results = {
        "Beam Deflection": (beam_root, beam_table, None),
        "Spring Equilibrium": (spring_root, spring_table, None),
    }
    plot_convergence(plot_results)


if __name__ == "__main__":
    main()