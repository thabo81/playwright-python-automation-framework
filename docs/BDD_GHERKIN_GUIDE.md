# BDD / Gherkin with Playwright

This guide documents the BDD layer added to the Python + Pytest + Playwright framework.

The project uses **pytest-bdd** to provide a Cucumber-style Gherkin specification layer while continuing to use the existing Pytest fixtures and Playwright Page Objects.

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

BDD is an additional specification layer. It does not replace normal Pytest tests or API tests.

## First Feature

The first feature is:

`features/login.feature`

It describes a successful user login in business-readable language:

```gherkin
@bdd
Feature: User login

  @smoke
  Scenario: Successful login redirects to the dashboard
    Given I am on the login page
    When I log in with valid credentials
    Then I should be redirected to the dashboard
```

## Step Definitions

The matching Python implementation lives in:

`tests/bdd/step_defs/login_steps.py`

The step definitions intentionally call the existing `LoginPage` Page Object instead of directly using selectors.

This keeps the responsibilities separated:

| Layer | Responsibility |
|---|---|
| Feature | Describe behaviour in business language |
| Step definition | Translate behaviour into test actions |
| Fixture | Provide reusable test context |
| Page Object | Encapsulate Playwright locators/actions |
| Playwright | Drive the browser |

## Running BDD Tests

Run the BDD test file:

```bash
pytest tests/bdd/test_login_bdd.py -v
```

Run only BDD scenarios using the marker:

```bash
pytest -m bdd -v
```

Run BDD smoke scenarios:

```bash
pytest -m "bdd and smoke" -v
```

## Why pytest-bdd Instead of Replacing Pytest

pytest-bdd implements a subset of Gherkin and integrates with Pytest fixtures, allowing existing setup and test infrastructure to be reused. This makes it suitable for this Python Playwright framework without introducing a separate test runner. citeturn441412search2

The project is therefore using **Cucumber-style BDD**, rather than replacing the Python stack with a separate Cucumber runtime.

## Dependency

The repository pins:

```text
pytest-bdd==9.0.0
```

Version 9.0.0 was released on September 30, 2026 and supports Python 3.10 through 3.14. citeturn441412search0turn441412search1

## Next BDD Milestones

1. Add successful-login scenario — completed.
2. Add invalid-login scenario.
3. Add empty-credentials scenario.
4. Add Scenario Outline / Examples for reusable login data.
5. Add BDD tags and selective execution.
6. Verify Allure reporting for BDD scenarios.
7. Execute BDD scenarios in GitHub Actions.
8. Refine the framework structure after the BDD layer is stable.
