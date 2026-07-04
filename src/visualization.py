"""
visualization.py

Generates convergence graphs (Error vs Iteration) for both applications
-- beam deflection and spring equilibrium -- side by side, and saves them
as an image file.
"""

import os
import matplotlib.pyplot as plt


def plot_convergence(results_dict, save_path="results/graphs/convergence_comparison.png"):
    """
    results_dict format: { "Label": (root, history_table, status), ... }
    Creates one subplot per application, all sharing the same figure.
    """
    names = list(results_dict.keys())
    fig, axes = plt.subplots(1, len(names), figsize=(6 * len(names), 5))
    if len(names) == 1:
        axes = [axes]

    colors = ["tab:blue", "tab:orange"]

    for ax, name, color in zip(axes, names, colors):
        _, table, _ = results_dict[name]
        ax.plot(table["Iteration"], table["Error"], marker="o", color=color, linewidth=2)
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
    plt.show()


if __name__ == "__main__":
    from application_beam import run_beam_application
    from application_spring import run_spring_application

    results = {
        "Beam Deflection": run_beam_application(verbose=False),
        "Spring Equilibrium": run_spring_application(verbose=False),
    }
    plot_convergence(results)