from pathlib import Path

from pytest_bdd import scenarios

# Register the dashboard step-definition module as a Pytest plugin.
# This exposes its Given/Then functions to pytest-bdd's step discovery.
pytest_plugins = ("tests.bdd.step_defs.dashboard_steps",)

# Resolve the feature file from the repository root so the path works
# regardless of the current working directory used to run Pytest.
FEATURE_FILE = (
    Path(__file__).resolve().parents[2] / "features" / "dashboard.feature"
)

# Generate Pytest test functions from all scenarios in dashboard.feature.
scenarios(str(FEATURE_FILE))
