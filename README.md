```markdown
# Newton-Raphson Solver for Nonlinear Engineering Problems

A general-purpose Newton-Raphson solver in Python that finds roots of nonlinear polynomial equations, applied to two mechanical engineering problems. Derivatives are computed automatically using SymPy.

## Project Structure

```
src/
  newton_raphson.py          # Core solver with 3 failure-mode checks
  application_beam.py        # App 1: beam deflection position
  application_spring.py      # App 2: nonlinear spring equilibrium
  utilities.py               # CSV export, equation validation, comparison table
  visualization.py           # Convergence graph (log-scale)
  main.py                    # Entry point — run this file
tests/
  test_newton_raphson.py     # 8 tests: correctness, failures, validation, order
  test_applications.py       # 2 integration tests
```

## Setup and Run

```bash
pip install -r requirements.txt
python src/main.py
```

Run tests: `python -m pytest`

## The Solver

Finds `f(x) = 0` using:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

- **Derivative:** Auto-computed by SymPy (no manual calculus)
- **Stopping rule:** `|x_{n+1} - x_n| < 10^{-6}`
- **Order tracking:** Standard empirical formula `p ≈ log(e_n/e_{n-1}) / log(e_{n-1}/e_{n-2})` — should trend toward 2.0

**Three built-in failure checks:**

| Failure | Detection |
|---|---|
| Flat slope (`f'(x) ≈ 0`) | Stops with clear message |
| Divergence to infinity | Stops with clear message |
| Oscillating cycle | Stops with clear message |

## Application 1: Beam Deflection

Simply supported beam, concentrated point load at center. Find position `x` where deflection equals a target value.

$$\delta(x) = \frac{Px(3L^2 - 4x^2)}{48EI}, \quad 0 \le x \le L/2$$

| Parameter | Value |
|---|---|
| L (span) | 6.0 m |
| P (load) | 15,000 N |
| E (steel) | 200 × 10⁹ Pa |
| I | 2 × 10⁻⁵ m⁴ |
| Target deflection | 0.005 m |

## Application 2: Nonlinear Spring Equilibrium

Cubic stiffening spring model: `F(x) = kx + βx³`. Find equilibrium displacement.

| Parameter | Value |
|---|---|
| k (linear) | 500 N/m |
| β (nonlinear) | 50 N/m³ |
| Applied force | 2000 N |

## Results

| Metric | Beam Deflection | Spring Equilibrium |
|---|---|---|
| Iterations | 4 | 4 |
| Root (x*) | 0.60062 m | 2.47814 m |
| Final error | 2.87 × 10⁻¹¹ | 3.55 × 10⁻⁷ |
| Order estimates | 2.12 → 2.00 | 1.92 → 2.00 |

Both converge in 4 iterations with order estimates confirming quadratic convergence (~2.0). The spring's nonlinear result (2.478 m) differs 38% from the linear prediction (4.0 m), showing the practical significance of the cubic stiffening term.

## Team

| Name | ID |
|---|---|
| Ghania Jawed | 62745 |
| Samia Shahzad | 64248 |
```