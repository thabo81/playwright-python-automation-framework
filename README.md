# Playwright Python Automation Framework

A hands-on SDET automation project built with **Python, Pytest, and Playwright**.

This repository documents my practical learning and implementation of modern web test automation, following the concepts covered in ***Web Automation with Playwright and Python using AI and MCP*** by Kailash Pathak.

The goal is to build a maintainable, production-style automation framework rather than a collection of isolated scripts.

## Tech Stack

* Python
* Pytest
* Playwright
* Git & GitHub
* GitHub Actions
* REST API testing
* API mocking
* Page Object Model (POM)
* Pytest-BDD / Gherkin
* Allure Report
* Pillow for screenshot comparison
* axe-playwright-python / axe-core for automated accessibility scans

## What This Project Covers

### UI Automation

* Browser automation with Playwright
* Locator strategies
* Assertions
* Auto-waiting
* Navigation and user interactions
* Form testing
* Authentication flows
* Cross-browser testing
* Screenshots, videos, traces, and debugging

### API Testing & Mocking

* API requests and responses
* API validation
* Request interception
* Mock API responses
* Test data control
* Combining API and UI automation

### Page Object Model

The framework uses the Page Object Model to separate:

* Test logic
* Page locators
* Page actions
* Reusable components

This improves readability, maintainability, and reusability as the test suite grows.

### BDD / Gherkin

The framework includes a Cucumber-style Gherkin layer using `pytest-bdd`. The login feature covers successful login plus a data-driven Scenario Outline for invalid-password and empty-credentials cases. A separate dashboard feature validates authenticated dashboard access, its title, and the personalized welcome message. The BDD milestone was verified in GitHub Actions with dashboard scenarios, tag-selection checks, Allure report generation, and evidence upload.

The BDD layer is intended to demonstrate:

* Feature files written in Gherkin
* Given / When / Then step definitions
* Business-readable scenarios
* BDD integration with existing Playwright Page Objects
* Reusable Pytest fixtures
* Allure reporting for BDD scenarios
* Running BDD scenarios through GitHub Actions

The intended architecture is:

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

BDD will complement the existing Pytest tests rather than replace technical/API-level tests.


## Visual Regression and Accessibility Testing

The framework now includes a screenshot-baseline comparison for the authenticated dashboard and an automated axe-core accessibility scan. Visual mismatches produce actual/diff images under `test-results/visual-diff/`; the CI workflow uploads these files with the other test evidence. See [Visual and Accessibility Testing](docs/VISUAL_AND_ACCESSIBILITY_TESTING.md) for baseline governance, scan limitations, and manual checks.

## Project Structure

```text
playwright-python-automation-framework/
├── features/
│   ├── login.feature
│   └── dashboard.feature
├── tests/
│   ├── api/
│   ├── ui/
│   └── bdd/
│       ├── step_defs/
│       │   ├── login_steps.py
│       │   └── dashboard_steps.py
│       ├── test_login_bdd.py
│       └── test_dashboard_bdd.py
├── pages/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── docs/
│   ├── BDD_GHERKIN_GUIDE.md
│   ├── VISUAL_AND_ACCESSIBILITY_TESTING.md
│   ├── PLAYWRIGHT_METHOD_REFERENCE.md
│   ├── GITHUB_ACTIONS_GUIDE.md
│   └── ALLURE_REPORTING_GUIDE.md
└── .github/
    └── workflows/
        └── tests.yml
```

As the BDD layer grows, we can add more feature files, scenarios, and shared step definitions.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/thabo81/playwright-python-automation-framework.git
cd playwright-python-automation-framework
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

### 5. Run the tests

```bash
pytest
```

## Example Test Command

Run a specific test file:

```bash
pytest tests/ui/test_login.py
```

Run tests with a visible browser:

```bash
pytest --headed
```

Run tests using a specific browser:

```bash
pytest --browser chromium
```

## CI/CD

GitHub Actions now automatically:

1. Installs Python dependencies with pip caching.
2. Installs Chromium and required Linux system dependencies.
3. Executes the Playwright test suite in parallel.
4. Generates an Allure HTML report.
5. Uploads the Allure report and raw test evidence as workflow artifacts.
6. Runs for pushes and pull requests targeting `main`.
7. Supports manual execution through `workflow_dispatch`.
8. Cancels superseded runs for the same branch or pull request.

The CI workflow runs the complete Pytest suite, separately verifies BDD tag filtering, generates an Allure HTML report, and uploads Allure results plus Playwright and visual-diff evidence. The latest execution status is available in [GitHub Actions](https://github.com/thabo81/playwright-python-automation-framework/actions).

Target workflow:

```text
Git Push / Pull Request
        ↓
GitHub Actions
        ↓
Install Dependencies
        ↓
Install Playwright
        ↓
Run Pytest
        ↓
Generate Test Report
        ↓
Upload Artifacts
```

## Learning Documentation

Use these references while working through the framework:

* [Playwright & Pytest Method Reference](docs/PLAYWRIGHT_METHOD_REFERENCE.md) — methods already used, methods planned for later stages, and quick recall by task.
* [GitHub Actions Setup Guide](docs/GITHUB_ACTIONS_GUIDE.md) — step-by-step instructions for writing, understanding, running, and debugging CI workflows.
* [Visual and Accessibility Testing](docs/VISUAL_AND_ACCESSIBILITY_TESTING.md) — implemented screenshot comparison, baseline updates, automated axe-core scans, and manual checks.

## Reporting & Test Evidence

The framework uses **Allure Report** for structured test reporting and **Playwright tracing** for browser-level failure diagnostics.

* [Allure Reporting Guide](docs/ALLURE_REPORTING_GUIDE.md) — how Allure results are generated, reported, and used in CI.
* [Playwright & Pytest Method Reference](docs/PLAYWRIGHT_METHOD_REFERENCE.md) — method lookup and quick recall.
* [GitHub Actions Setup Guide](docs/GITHUB_ACTIONS_GUIDE.md) — CI workflow construction and debugging.

## Learning Roadmap

* [x] Set up Python environment
* [x] Set up Playwright with Pytest
* [x] Learn Playwright locators and assertions
* [x] Build reusable Pytest fixtures
* [x] Implement Page Object Model
* [x] Add UI test scenarios
* [x] Add API tests
* [x] Implement API mocking and request interception
* [x] Add authentication and reusable test state
* [x] Add parallel execution
* [x] Add reporting and tracing
* [x] Add GitHub Actions CI/CD and verify successful workflow execution
* [x] Verify Pytest-BDD step discovery and run the first scenario successfully
* [x] Create the first Cucumber-style Gherkin login feature and step definitions
* [x] Add invalid-password and empty-credentials scenarios
* [x] Verify the expanded BDD scenarios through GitHub Actions
* [x] Add Scenario Outline / Examples for data-driven BDD tests
* [x] Verify the Scenario Outline revision in GitHub Actions
* [x] Verify BDD tag filtering in GitHub Actions
* [x] Inspect Allure report for Gherkin scenario names and labels
* [x] Add and verify a Gherkin Background for shared login setup
* [x] Add a separate dashboard feature using authenticated fixtures and the DashboardPage
* [x] Verify dashboard BDD scenarios through GitHub Actions (12-test suite passed)
* [x] Document visual-regression and accessibility-testing next steps
* [x] Implement screenshot comparison against a committed dashboard baseline using Pillow
* [x] Produce actual and highlighted diff screenshots when a visual check fails
* [x] Add automated axe-core accessibility scanning to the dashboard test suite
* [x] Document manual accessibility checks and baseline review/update governance
* [ ] Build a complete end-to-end automation project in a separate real-application suite

## Testing Strategy

The framework will apply core software testing principles such as:

* Equivalence Partitioning
* Boundary Value Analysis
* Positive and negative testing
* Functional testing
* Regression testing
* End-to-end testing
* API testing
* Visual regression testing (dashboard screenshot baseline comparison)
* Accessibility testing (automated axe-core scan plus documented manual assessment)
* Risk-based test coverage

BDD will add a business-readable specification layer on top of these technical testing practices.

## Quality Goals

This project focuses on:

* Reliable and deterministic tests
* Reusable automation components
* Clear test naming
* Maintainable framework architecture
* Strong test isolation
* Useful failure diagnostics
* CI-friendly execution
* Clean and typed Python code
* Business-readable BDD scenarios

## Portfolio Purpose

This repository is part of my **SDET portfolio** and demonstrates practical experience with:

**Python + Pytest + Playwright + BDD/Gherkin + UI Automation + API Testing + Mocking + POM + CI/CD + Allure**

Visual-regression comparison and automated accessibility scanning are implemented for the demo dashboard. These checks complement functional tests; they do not replace full manual accessibility assessment or comprehensive visual coverage across a real application.

The repository will evolve as new automation concepts and projects are implemented.

## Learning Resource

**Web Automation with Playwright and Python using AI and MCP**
Author: **Kailash Pathak**

This book is being used as a learning reference while building the framework and applying the concepts through practical automation.

## Author

**Thabo81**

GitHub: [@thabo81](https://github.com/thabo81)
