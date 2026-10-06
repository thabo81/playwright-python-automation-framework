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

## Planned Project Structure

```text
playwright-python-automation-framework/
├── tests/
│   ├── ui/
│   └── api/
├── pages/
├── fixtures/
├── utils/
├── test_data/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── .gitignore
├── README.md
└── .github/
    └── workflows/
        └── tests.yml
```

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

GitHub Actions will be used to automatically:

1. Install Python dependencies.
2. Install Playwright browsers.
3. Execute the automated test suite.
4. Generate test results.
5. Preserve relevant test artifacts such as reports and traces.

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
* [ ] Add GitHub Actions CI/CD and verify successful workflow execution
* [ ] Build a complete end-to-end automation project

## Testing Strategy

The framework will apply core software testing principles such as:

* Equivalence Partitioning
* Boundary Value Analysis
* Positive and negative testing
* Functional testing
* Regression testing
* End-to-end testing
* API testing
* Risk-based test coverage

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

## Portfolio Purpose

This repository is part of my **SDET portfolio** and demonstrates practical experience with:

**Python + Pytest + Playwright + UI Automation + API Testing + Mocking + POM + CI/CD**

The repository will evolve as new automation concepts and projects are implemented.

## Learning Resource

**Web Automation with Playwright and Python using AI and MCP**
Author: **Kailash Pathak**

This book is being used as a learning reference while building the framework and applying the concepts through practical automation.

## Author

**Thabo81**

GitHub: [@thabo81](https://github.com/thabo81)
