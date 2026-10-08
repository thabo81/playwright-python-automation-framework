from pathlib import Path

from pytest_bdd import scenarios

# Import the individual step functions into this test module.
# pytest-bdd discovers decorated step functions through the module's
# fixture namespace, so importing the functions explicitly is important.
from tests.bdd.step_defs.login_steps import (  # noqa: F401
    user_is_on_login_page,
    user_logs_in_with_valid_credentials,
    user_should_reach_dashboard,
)


# Resolve the feature file from the repository root rather than relying
# on the current working directory used by the test runner.
FEATURE_FILE = (
    Path(__file__).resolve().parents[2] / "features" / "login.feature"
)

# Generate Pytest test functions from the Gherkin feature file.
scenarios(str(FEATURE_FILE))
