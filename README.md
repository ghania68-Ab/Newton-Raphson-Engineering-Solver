# Newton-Raphson Solver for Nonlinear Engineering Problems

## What this project does

Many engineering problems cannot be solved with simple algebra because the equations are **nonlinear**. This project builds a general-purpose **Newton-Raphson solver** in Python that finds the root (solution) of any nonlinear polynomial equation, and applies it to two real engineering problems.

The derivative needed by the Newton-Raphson formula is computed **automatically** using the SymPy library, so no manual calculus is required in the code. Every equation is also validated before solving, so a typo or an unexpected symbol produces a clear error message instead of a raw crash.

---

## Project Structure

| File | What it does |
|---|---|
| `newton_raphson.py` | The core solver. Works for any equation, checks for 3 common failure cases, and estimates the empirical order of convergence at each step. |
| `application_beam.py` | Application 1 — finds where a beam reaches an allowable deflection. |
| `application_spring.py` | Application 2 — finds the equilibrium displacement of a nonlinear spring. |
| `utilities.py` | Helper functions — CSV export, equation validation, comparison table printing. |
| `visualization.py` | Draws the convergence graphs for both applications (scales automatically to any number of applications). |
| `main.py` | Runs everything in one go. This is the file you actually execute. |
| `tests/test_newton_raphson.py` | Pytest checks for the solver's core behavior and all safety checks. |
| `tests/test_applications.py` | Pytest checks confirming both engineering applications converge correctly. |

---

## How to Install

| Step | Command / Action |
|---|---|
| 1. Open a terminal in the project folder | — |
| 2. Install the required packages | `pip install -r requirements.txt` |

`pytest` is only needed for automated testing. The main project still runs with `python src/main.py`.

---

## How to Run

Just run one command:

```bash
python src/main.py
```

This automatically:
1. Solves the beam deflection problem
2. Solves the spring equilibrium problem
3. Prints the iteration table for each (including error and order-of-convergence estimates)
4. Saves both tables as CSV files
5. Prints a side-by-side comparison summary
6. Generates and saves a convergence graph

| Output | Saved to |
|---|---|
| Iteration tables (CSV) | `results/iteration_tables/` |
| Convergence graph (PNG) | `results/graphs/` |

The project uses one combined convergence comparison graph:

```text
results/graphs/convergence_comparison.png
```

This file contains separate subplots for the beam and spring applications, so both convergence patterns can be compared in one figure.

---

## Optional Automated Tests

The project includes a pytest test suite covering both the solver and the engineering applications. These tests are not part of the main program, but they confirm everything is working correctly.

Run all tests with:

```bash
python -m pytest
```

**Solver tests (`test_newton_raphson.py`) check that:**
1. The solver finds the known root of `x**3 - x - 2`, approximately `1.52138`.
2. The zero-derivative check stops cleanly.
3. The divergence check stops cleanly.
4. The cycle/oscillation check stops cleanly.
5. Invalid settings (`tol <= 0`, `max_iter <= 0`) are rejected with a clear message.
6. Equations containing unknown symbols (e.g. `x**2 + y`) are rejected by `validate_equation`.

**Application tests (`test_applications.py`) check that:**
1. The beam deflection application converges and returns a valid, non-empty iteration table.
2. The spring equilibrium application converges and returns a valid, non-empty iteration table.

---

## How the Solver Works

Newton-Raphson finds the root of `f(x) = 0` using this formula, repeated until the answer stops changing:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

| Setting | Value |
|---|---|
| Stopping rule | Stop when the change between steps is smaller than `0.000001` |
| Derivative | Computed automatically by SymPy — no manual calculus |
| Equation input | Validated first — only the symbol `x` is allowed, and invalid expressions are rejected with a clear error |

**The solver also checks for 3 ways Newton-Raphson can fail**, so it never crashes silently:

| Problem | What the solver does |
|---|---|
| The slope is flat (`f'(x) ≈ 0`) | Stops and reports it instead of dividing by zero |
| The answer runs away to infinity | Stops and reports divergence |
| The answer gets stuck bouncing between two values | Stops and reports the cycle |

The solver also returns a clear message if the maximum number of iterations is reached before convergence, or if the given `tol`/`max_iter` settings are invalid.

**Order of convergence:** each iteration row also reports an *empirical order estimate*, calculated as `log(error_n+1) / log(error_n)`. Newton-Raphson is theoretically a second-order (quadratic) method, so this value should trend toward **2.0** as the solution converges. In practice, both applications in this project show the order estimate settling into the 2.2–2.6 range within a few iterations, confirming the expected quadratic behavior.

---

## Code Quality and Robustness Updates

The final code was improved without changing the main project structure:

1. Type hints were added to function signatures.
2. `main.py` now handles application errors safely, so one failed application does not stop the other one from running.
3. The Newton-Raphson solver returns clear status messages for convergence, zero derivative, divergence, oscillation, invalid settings, and maximum iterations.
4. All equation strings are validated (`utilities.validate_equation`) before being solved, catching typos and disallowed symbols with a readable error instead of a raw SymPy traceback.
5. Each iteration now records both a rounded error (for display) and a raw, unrounded error (for accurate final-error reporting in the comparison table).
6. An empirical order-of-convergence estimate is computed and logged at every iteration.
7. The convergence graph automatically scales its color palette to any number of applications, instead of being hardcoded to exactly two.
8. Automated tests were expanded to cover invalid solver settings, equation validation, and both engineering applications directly — not just the core solver.
9. The requirements file was updated to match the imports used by the project.

---

## Application 1: Beam Deflection

A simply supported beam has a **concentrated point load** at its center. We want to know the position `x` along the beam where it reaches a target (allowable) deflection.

$$\delta(x) = \frac{P \cdot x \cdot (3L^2 - 4x^2)}{48EI}$$

Setting this equal to the target deflection gives a **cubic equation** — solvable using only the power rule.

> **Note:** a uniformly distributed load (UDL) produces a *quartic* deflection equation, which would require a derivative beyond the power rule alone. A concentrated point load was used instead so the problem stays cubic and consistent with the project's design goal of using only power-rule derivatives, while still representing a genuine, non-trivial engineering scenario.

| Parameter | Value |
|---|---|
| Beam length (L) | 6.0 m |
| Point load (P) | 15,000 N |
| Young's modulus (E) | 200 × 10⁹ Pa (steel) |
| Moment of inertia (I) | 2 × 10⁻⁵ m⁴ |
| Target deflection | 0.005 m (5 mm) |

---

## Application 2: Spring-Mass Equilibrium

A real spring doesn't always stretch in a straight line. This model adds a small **cubic stiffening term** to the usual spring force:

$$F(x) = kx + \beta x^3$$

At equilibrium, this force balances the applied load, giving a **cubic equation** in `x`.

| Parameter | Value |
|---|---|
| Linear spring constant (k) | 500 N/m |
| Nonlinear stiffening term (β) | 50 N/m³ |
| Applied force | 2000 N |

---

## Results

| Metric | Beam Deflection | Spring Equilibrium |
|---|---|---|
| Equation type | Cubic | Cubic |
| Initial guess (x₀) | 1.00 m | 2.00 m |
| Iterations to converge | 4 | 4 |
| Final root (x*) | 0.60062 m | 2.47814 m |
| Final error (unrounded) | 2.87 × 10⁻¹¹ | 3.55 × 10⁻⁷ |
| Physically valid? | Yes (within 0 – 3.0 m span) | Yes (positive displacement) |

**What this shows:** both problems converge in just 4 iterations, and the error shrinks very fast with each step — this is the "quadratic convergence" that makes Newton-Raphson so much faster than simpler methods like Bisection. The order-of-convergence estimates in both iteration tables trend toward ~2.0, confirming this behavior numerically rather than just by iteration count.

Interestingly, although both applications converge in the same number of iterations, the beam problem reaches a noticeably smaller final error (2.87 × 10⁻¹¹) than the spring problem (3.55 × 10⁻⁷). Both are comfortably below the tolerance of 1 × 10⁻⁶, but the difference shows that "same iteration count" doesn't always mean "identical convergence quality" — a useful comparison point between the two applications.

For the spring, a purely linear spring (ignoring the cubic term) would predict a displacement of 4.0 m — the real answer of 2.478 m shows how much the nonlinear stiffening term actually matters.

---

## Team Members

| Name | ID |
|---|---|
| [Ghania Jawed] | [62745] |
| [Samia Shahzad] | [64248] |