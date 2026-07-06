import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from application_beam import run_beam_application
from application_spring import run_spring_application


def test_beam_application_converges() -> None:
    root, table, status = run_beam_application(verbose=False)

    assert root is not None
    assert "Converged" in status
    assert not table.empty


def test_spring_application_converges() -> None:
    root, table, status = run_spring_application(verbose=False)

    assert root is not None
    assert "Converged" in status
    assert not table.empty