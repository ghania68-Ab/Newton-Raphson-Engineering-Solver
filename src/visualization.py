"""
visualization.py

Generates convergence graphs (Error vs Iteration) for both applications
-- beam deflection and spring equilibrium -- side by side, and saves them
as an image file.

Uses matplotlib's tab10 colormap instead of a hardcoded color list, so
the plot automatically scales to any number of applications (up to 10)
without needing code changes if a third or fourth application is added
later.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_convergence(results_dict: dict[str, tuple[float | None, pd.DataFrame, str | None]], save_path: str = "results/graphs/convergence_comparison.png") -> None:
    """
    results_dict format: { "Label": (root, history_table, status), ... }
    Creates one subplot per application, all sharing the same figure.
    """
    names = list(results_dict.keys())
    fig, axes = plt.subplots(1, len(names), figsize=(6 * len(names), 5))
    if len(names) == 1:
        axes = [axes]

    colors = plt.cm.tab10.colors  # supports up to 10 applications automatically

    for ax, name, color in zip(axes, names, colors):
        _, table, _ = results_dict[name]
        ax.plot(table["Iteration"], table["Raw Error"], marker="o", color=color, linewidth=2)
        ax.set_title(name)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Error")
        ax.set_yscale("log")
        ax.grid(True, which="both", linestyle="--", alpha=0.5)

    fig.suptitle("Newton-Raphson Convergence Comparison", fontsize=14, fontweight="bold")
    plt.tight_layout()

    save_dir = os.path.dirname(save_path)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
    plt.savefig(save_path, dpi=150)
    print(f"\nGraph saved as: {save_path}")
    if "agg" not in plt.get_backend().lower():
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    from application_beam import run_beam_application
    from application_spring import run_spring_application

    results = {
        "Beam Deflection": run_beam_application(verbose=False),
        "Spring Equilibrium": run_spring_application(verbose=False),
    }
    plot_convergence(results)