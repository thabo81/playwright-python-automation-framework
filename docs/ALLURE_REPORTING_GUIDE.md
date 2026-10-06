# Allure Reporting for Pytest + Playwright

This document explains how this repository generates and consumes Allure test reports.

Allure has two parts in this project:

1. `allure-pytest` — the Python/Pytest integration that writes test result files.
2. Allure Report 3 CLI — the command-line tool that converts those result files into an HTML report.

The official Allure Pytest documentation uses `--alluredir` to write results and `allure generate` or `allure serve` to create/view the report.

## 1. Install the Pytest integration

The project dependency is:

```text
allure-pytest==2.16.2
```

Install everything with:

```bash
pip install -r requirements.txt
```

## 2. How pytest.ini is configured

This repository uses:

```ini
[pytest]
addopts = -ra --alluredir=allure-results --clean-alluredir --tracing=retain-on-failure
```

The important options are:

| Option | Purpose |
|---|---|
| `--alluredir=allure-results` | Writes Allure result files into `allure-results/`. |
| `--clean-alluredir` | Removes results from the previous run before creating the new result set. |
| `--tracing=retain-on-failure` | Keeps Playwright traces when tests fail. |

Because these options are in `pytest.ini`, a normal `pytest` command now produces Allure results automatically.

## 3. Run the tests locally

Run the complete suite:

```bash
pytest
```

Or run with two workers:

```bash
pytest --numprocesses 2
```

The tests still execute through the same Pytest/Playwright framework.

After the run, you should see:

```text
allure-results/
test-results/
```

## 4. Install Allure Report 3 locally

Allure Report 3 is installed using Node.js.

Check Node.js:

```bash
node --version
```

Install Allure:

```bash
npm install -g allure
```

Check the installation:

```bash
allure --version
```

Allure's current installation documentation recommends Node.js and the `allure` npm package for Allure Report 3.

## 5. Generate an HTML report

After running the tests:

```bash
allure generate ./allure-results
```

This converts the raw Allure result files into an HTML report directory:

```text
allure-results/
        ↓
allure generate
        ↓
allure-report/
```

## 6. Open the report

Use:

```bash
allure open ./allure-report
```

This serves the generated report so it can be viewed in a browser.

Another development option is:

```bash
allure serve allure-results
```

That creates a temporary report and serves it directly.

## 7. What the report gives you

Allure is useful because a raw Pytest result such as:

```text
7 passed in 2.14s
```

does not tell the complete testing story.

The Allure report can provide:

- Test status
- Test duration
- Suites
- Test details and metadata
- Failure information
- Attachments
- Trends/history when configured
- Test categories
- Steps when Allure steps are added

## 8. Adding readable Allure metadata

Allure can add metadata such as titles, descriptions, severity, owners, links, and labels.

Example:

```python
import allure
import pytest


@allure.title("Valid user can log in")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
def test_valid_login(...) -> None:
    # Test implementation goes here.
    ...
```

### Method Reference

| Method / decorator | What it does |
|---|---|
| `@allure.title()` | Sets the human-readable title in the report. |
| `@allure.description()` | Adds a test description. |
| `@allure.severity()` | Assigns a severity such as critical, blocker, normal, minor, or trivial. |
| `@allure.tag()` | Adds a report tag. |
| `@allure.link()` | Adds a related URL. |
| `@allure.issue()` | Links a test to an issue identifier when configured. |
| `allure.step()` | Creates a named step visible in the report. |
| `allure.attach()` | Adds text, bytes, or files as report attachments. |

Use these features where they add useful test information; do not decorate every line of a test.

## 9. Add readable steps

Example:

```python
import allure


def test_login(...) -> None:
    with allure.step("Open the login page"):
        # Navigate to the application.
        ...

    with allure.step("Enter valid credentials"):
        # Enter username and password.
        ...

    with allure.step("Verify dashboard is displayed"):
        # Assert successful authentication.
        ...
```

The method:

```python
with allure.step("...")
```

creates a named step in the generated report.

## 10. Why tracing is separate from Allure

Allure answers:

```text
What tests ran?
What passed?
What failed?
How long did they take?
What evidence was attached?
```

Playwright tracing answers a different question:

```text
What exactly happened inside the browser?
```

That makes the combination useful:

```text
Allure Report
     +
Playwright Trace
     +
Screenshot
     +
Pytest output
```

Together they provide much stronger failure diagnostics.

## 11. CI flow

The GitHub Actions workflow now follows:

```text
Checkout
   ↓
Python
   ↓
Node.js
   ↓
Python dependencies
   ↓
Playwright Chromium + OS dependencies
   ↓
Allure CLI
   ↓
pytest
   ↓
allure-results/
   ↓
allure generate
   ↓
allure-report/
   ↓
GitHub Actions artifact
```

The workflow uses `if: always()` for report generation and evidence upload so the report-building steps can still run after a test failure.

## 12. Why we do not commit the report

The repository ignores:

```text
allure-results/
allure-report/
test-results/
```

These directories are generated output, not source code.

The CI workflow stores them as GitHub Actions artifacts instead.

## 13. Current learning experiment

For the current seven-test suite we observed:

```text
Serial:
7 passed in 2.14s

2 workers:
7 passed in 3.82s
```

This is not a failure of xdist.

A small suite can become slower because worker startup and inter-process coordination cost more than the time saved by concurrency.

The useful engineering lesson is:

> Parallelization should be measured against the workload, not assumed to be faster.

As the suite becomes larger and contains slower tests, we can measure the benefit again.

## Official References

Allure Pytest:
https://allurereport.org/docs/pytest/

Allure Pytest configuration:
https://allurereport.org/docs/pytest-configuration/

Allure Report 3 installation:
https://allurereport.org/docs/v3/install/

Allure GitHub Actions:
https://allurereport.org/docs/integrations-github-action/

## 14. Viewing Allure in GitHub Codespaces

When using GitHub Codespaces, `allure open` may start a local server on a port that is not forwarded correctly to the browser.

Use the generated static report with Python's built-in HTTP server instead:

```bash
npx allure generate ./allure-results
python -m http.server 8080 --bind 0.0.0.0 --directory allure-report
```

Then open the Codespaces **Ports** panel and forward port `8080`.

Use **Open in Browser** for the forwarded port.

### Why this works

```text
allure-results/
      ↓
Allure Report 3
      ↓
allure-report/
      ↓
Python HTTP server
      ↓
0.0.0.0:8080
      ↓
Codespaces forwarded port
      ↓
Browser
```

Keep the terminal running while viewing the report. Stop the server with:

```text
Ctrl+C
```

This approach is useful specifically for Codespaces because the report is a static HTML application served through a known forwarded port.

