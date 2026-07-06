import math
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from newton_raphson import newton_raphson
from utilities import validate_equation


def test_solver_finds_known_root() -> None:
    result = newton_raphson("x**3 - x - 2", x0=1.5)

    assert result["converged"] is True
    assert math.isclose(result["root"], 1.52138, rel_tol=0, abs_tol=1e-5)


def test_zero_derivative_check_stops_cleanly() -> None:
    result = newton_raphson("x**3", x0=0.0)

    assert result["converged"] is False
    assert result["root"] is None
    assert "derivative" in result["status"]


def test_divergence_check_stops_cleanly() -> None:
    result = newton_raphson("1e-11*x + 1", x0=0.0, max_iter=10)

    assert result["converged"] is False
    assert result["root"] is None
    assert "diverged" in result["status"]


def test_cycle_check_stops_cleanly() -> None:
    result = newton_raphson("x**3 - 5*x", x0=1.0, max_iter=10)

    assert result["converged"] is False
    assert result["root"] is None
    assert "cycle" in result["status"]


def test_tolerance_must_be_positive() -> None:
    result = newton_raphson("x**3 - x - 2", x0=1.5, tol=0)

    assert result["converged"] is False
    assert result["root"] is None
    assert "tolerance" in result["status"]


def test_max_iter_must_be_positive() -> None:
    result = newton_raphson("x**3 - x - 2", x0=1.5, max_iter=0)

    assert result["converged"] is False
    assert result["root"] is None
    assert "max_iter" in result["status"]


def test_validate_equation_rejects_unknown_symbol() -> None:
    with pytest.raises(ValueError):
        validate_equation("x**2 + y")