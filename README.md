# Newton-Raphson Solver for Nonlinear Engineering Problems

## What this project does

Many engineering problems cannot be solved with simple algebra because the equations are **nonlinear**. This project builds a general-purpose **Newton-Raphson solver** in Python that finds the root (solution) of any nonlinear polynomial equation, and applies it to two real engineering problems.

The derivative needed by the Newton-Raphson formula is computed **automatically** using the SymPy library, so no manual calculus is required in the code.

---

## Project Structure

| File | What it does |
|---|---|
| `newton_raphson.py` | The core solver. Works for any equation, and checks for 3 common failure cases. |
| `application_beam.py` | Application 1 — finds where a beam reaches an allowable deflection. |
| `application_spring.py` | Application 2 — finds the equilibrium displacement of a nonlinear spring. |
| `utilities.py` | Small helper functions (saving CSV files, printing comparison tables). |
| `visualization.py` | Draws the convergence graphs for both applications. |
| `main.py` | Runs everything in one go. This is the file you actually execute. |

---

## How to Install

| Step | Command / Action |
|---|---|
| 1. Install Python 3.8 or newer | Download from [python.org](https://www.python.org/downloads/) |
| 2. Open a terminal in the project folder | — |
| 3. Install the required packages | `pip install -r requirements.txt` |

**requirements.txt:**
```
numpy>=1.20.0
pandas>=1.3.0
sympy>=1.8
matplotlib>=3.4.0
```

---

## How to Run

Just run one command:

```bash
python main.py
```

This automatically:
1. Solves the beam deflection problem
2. Solves the spring equilibrium problem
3. Prints the iteration table for each
4. Saves both tables as CSV files
5. Prints a side-by-side comparison summary
6. Generates and saves a convergence graph

| Output | Saved to |
|---|---|
| Iteration tables (CSV) | `results/iteration_tables/` |
| Convergence graph (PNG) | `results/graphs/` |

---

## How the Solver Works

Newton-Raphson finds the root of `f(x) = 0` using this formula, repeated until the answer stops changing:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

| Setting | Value |
|---|---|
| Stopping rule | Stop when the change between steps is smaller than `0.000001` |
| Derivative | Computed automatically by SymPy — no manual calculus |

**The solver also checks for 3 ways Newton-Raphson can fail**, so it never crashes silently:

| Problem | What the solver does |
|---|---|
| The slope is flat (`f'(x) ≈ 0`) | Stops and reports it instead of dividing by zero |
| The answer runs away to infinity | Stops and reports divergence |
| The answer gets stuck bouncing between two values | Stops and reports the cycle |

---

## Application 1: Beam Deflection

A simply supported beam has a **concentrated point load** at its center. We want to know the position `x` along the beam where it reaches a target (allowable) deflection.

$$\delta(x) = \frac{P \cdot x \cdot (3L^2 - 4x^2)}{48EI}$$

Setting this equal to the target deflection gives a **cubic equation** — solvable using only the power rule.

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
| Physically valid? | Yes (within 0 – 3.0 m span) | Yes (positive displacement) |

**What this shows:** both problems converge in just 4 iterations, and the error shrinks very fast with each step — this is the "quadratic convergence" that makes Newton-Raphson so much faster than simpler methods like Bisection.

For the spring, a purely linear spring (ignoring the cubic term) would predict a displacement of 4.0 m — the real answer of 2.478 m shows how much the nonlinear stiffening term actually matters.

---

## Team Members

| Name | ID |
|---|---|
| [Ghania Jawed] | [62745] |
| [Samia Shahzad] | [64248] |