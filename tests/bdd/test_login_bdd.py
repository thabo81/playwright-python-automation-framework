from pathlib import Path

# Import the step definitions so pytest-bdd registers the Given/When/Then
# bindings before the Gherkin scenarios are generated.
from tests.bdd.step_defs import login_steps  # noqa: F401
from pytest_bdd import scenarios


# Resolve the feature file from the repository root rather than relying
# on the current working directory used by the test runner.
FEATURE_FILE = (
    Path(__file__).resolve().parents[2] / "features" / "login.feature"
)

# Generate Pytest test functions from the Gherkin feature file.
scenarios(str(FEATURE_FILE))
