# BDD / Gherkin with Playwright

This guide documents the Cucumber-style BDD layer in the Python + Pytest + Playwright framework.

The project uses **pytest-bdd** to connect Gherkin feature files to Pytest fixtures and existing Playwright Page Objects. It complements ordinary Pytest UI/API tests; it does not replace them.

## Architecture

```text
Gherkin Feature
      ↓
Step Definitions
      ↓
Pytest Fixtures
      ↓
Page Objects
      ↓
Playwright
      ↓
Browser
```

## Login Feature

The feature file is `features/login.feature`. It describes three authentication behaviours:

1. Successful login redirects to the dashboard.
2. An invalid password is rejected with a clear error.
3. Empty credentials are rejected with a required-fields error.

Gherkin describes expected behaviour, without embedding Playwright selectors or browser operations in the feature file.

## Step Definitions and Plugin Registration

The Python implementations live in `tests/bdd/step_defs/login_steps.py`.

The scenario module `tests/bdd/test_login_bdd.py` registers the separate step-definition module using Pytest's `pytest_plugins` setting:

```python
# Register the module so Pytest can discover its decorated step definitions.
pytest_plugins = ("tests.bdd.step_defs.login_steps",)
```

A normal Python import alone does not guarantee that a separate module's step functions are registered as Pytest fixtures. Registering the module as a plugin makes the step definitions discoverable by pytest-bdd.

## Reusable Error Step

Both negative scenarios use one parameterized Gherkin step:

```gherkin
Then I should see the login error "Invalid username or password"
```

The step definition uses `parsers.parse(...)` to capture the quoted message as an argument. It passes that value to `LoginPage.assert_login_error()`, so the assertion and locator remain inside the Page Object.

## Run the BDD Scenarios

Run only the BDD scenario module:

```bash
pytest tests/bdd/test_login_bdd.py -v
```

Run scenarios tagged as BDD:

```bash
pytest -m bdd -v
```

Run the BDD smoke scenario:

```bash
pytest -m "bdd and smoke" -v
```

The feature-level `@bdd` tag and scenario-level `@smoke` tag make it possible to select groups of behaviours when invoking Pytest.

## Methods and Pytest-BDD Constructs Used

| Method / construct | Purpose |
|---|---|
| `@given(...)` | Maps a Gherkin Given step to a Python function. |
| `@when(...)` | Maps a Gherkin When step to a Python function. |
| `@then(...)` | Maps a Gherkin Then step to a Python function. |
| `parsers.parse(...)` | Extracts a value from a parameterized step sentence. |
| `pytest_plugins` | Registers a separate module as a Pytest plugin. |
| `scenarios(...)` | Generates Pytest test functions from scenarios in a feature file. |
| `login_page.open(...)` | Navigates through the existing LoginPage Page Object. |
| `login_page.login(...)` | Fills and submits the username and password fields. |
| `login_page.assert_login_error(...)` | Checks visibility and exact text of the login error. |
| `page.wait_for_url(...)` | Waits for the expected successful-login URL. |

## CI and Reporting

GitHub Actions runs the complete Pytest suite, including BDD scenarios discovered under `tests/`. The workflow generates an Allure report and uploads the report and test evidence as artifacts even when the test step fails.

The first BDD scenario was verified in CI as part of an eight-test pass. The expanded negative-scenario suite must pass in its own workflow run before this milestone is considered complete.

## References

- pytest-bdd documentation: https://pytest-bdd.readthedocs.io/
- Playwright Python CI: https://playwright.dev/python/docs/ci
- GitHub Actions documentation: https://docs.github.com/actions
