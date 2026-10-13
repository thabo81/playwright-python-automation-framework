from pathlib import Path

from pytest_bdd import scenarios

# Register the separate step-definition module as a Pytest plugin.
# This tells Pytest to discover its decorated Given/When/Then definitions
# as fixtures instead of merely importing Python function names.
pytest_plugins = ("tests.bdd.step_defs.login_steps",)

# Resolve the feature file from the repository root rather than relying
# on the current working directory used by the test runner.
FEATURE_FILE = (
    Path(__file__).resolve().parents[2] / "features" / "login.feature"
)

# Generate Pytest test functions from the Gherkin feature file.
scenarios(str(FEATURE_FILE))
