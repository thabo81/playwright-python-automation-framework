# GitHub Actions for Playwright — Step-by-Step Guide

This guide explains how to write, understand, run, and debug a GitHub Actions workflow for this Python + Pytest + Playwright project.

The goal is to understand the YAML rather than copy a workflow without knowing what each section does.

Playwright's current Python CI guidance uses GitHub Actions to check out the repository, install Python and project dependencies, install Playwright browsers plus operating-system dependencies, run Pytest, and optionally preserve traces/results as artifacts.

---

# 1. What CI Does

Local testing:

    Developer
        ↓
    Change code
        ↓
    pytest
        ↓
    Push code

Continuous integration:

    git push / pull request
        ↓
    GitHub Actions
        ↓
    Create clean runner
        ↓
    Checkout repository
        ↓
    Install Python
        ↓
    Install dependencies
        ↓
    Install Playwright + browser dependencies
        ↓
    Run Pytest
        ↓
    Pass / fail
        ↓
    Preserve diagnostics when required

The CI environment is therefore an independent validation environment.

For this repository, the workflow also uses:
- `workflow_dispatch` for manual runs.
- `concurrency` to cancel superseded runs for the same branch or pull request.
- pip caching through `actions/setup-python`.

---

# 2. Where the Workflow File Goes

Create this directory:

    .github/workflows/

Create the workflow file:

    .github/workflows/tests.yml

GitHub automatically detects workflow files stored in this location.

---

# 3. Write the Workflow Name

Start with:

    name: Playwright Tests

This is the name displayed in the GitHub Actions interface.

It does not determine how the tests execute.

---

# 4. Define the Trigger

Write:

    on:
      push:
        branches: ["main"]
      pull_request:
        branches: ["main"]
      workflow_dispatch:

Meaning:

| YAML section | Purpose |
|---|---|
| on | Defines workflow triggers. |
| push | Run after a push event. |
| pull_request | Run when a PR targets the selected branch. |
| branches | Limits the trigger to the specified branch. |

For this repository:

    Push to main
        ↓
    CI runs

    Pull request → main
        ↓
    CI runs

---

# 5. Create the Job

Write:

    jobs:
      test:

jobs is the container for the work GitHub will perform.

test is the identifier for our job.

Later we could have multiple jobs:

    jobs:
      lint:
      api-tests:
      ui-tests:
      security:

We start with one test job to keep the architecture understandable.

---

# 6. Choose the Runner

Write:

    jobs:
      test:
        timeout-minutes: 60
        runs-on: ubuntu-latest

runs-on selects the machine that executes the job.

Ubuntu is a practical choice for this project because Playwright's Python CI examples use a GitHub-hosted Ubuntu runner and install browser/system dependencies using Playwright's CLI.

timeout-minutes prevents a stuck job from consuming runner time indefinitely.

---

# 7. Understand steps

Everything the job performs lives under:

    steps:

Think of steps as an ordered test-environment setup:

    1. Checkout code
    2. Install Python
    3. Install Python packages
    4. Install Playwright browsers/dependencies
    5. Run tests
    6. Upload diagnostics

---

# 8. Checkout the Repository

Use:

    - name: Checkout repository
      uses: actions/checkout@v6

Why?

The GitHub runner starts clean.

The runner needs your repository files before it can execute:

    tests/
    pages/
    conftest.py
    pytest.ini
    requirements.txt

The checkout action makes those files available to later steps.

---

# 9. Install Python

Write:

    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: "3.13"

Important fields:

| Field | Purpose |
|---|---|
| name | Human-readable step name. |
| uses | Calls an existing GitHub Action. |
| with | Supplies configuration to that action. |
| python-version | Selects the Python runtime. |

For this learning project we use Python 3.13 in CI.

---

# 10. Install Project Dependencies

Write:

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

The run key executes shell commands on the runner.

First:

    python -m pip install --upgrade pip

updates pip.

Then:

    pip install -r requirements.txt

installs the packages declared by the repository.

---

# 11. Install Playwright Browsers and System Dependencies

Write:

    - name: Install Playwright browsers and dependencies
      run: python -m playwright install --with-deps chromium

This is critical on Linux CI runners.

The command installs:

    Playwright browser
        +
    required Linux browser dependencies

We previously encountered this class of problem locally when Chromium could not start because a Linux shared library was missing.

Playwright's CI documentation recommends installing browsers with system dependencies in CI environments.

---

# 12. Run Pytest

Basic version:

    - name: Run tests
      run: pytest --browser chromium

This causes GitHub to execute the same logical automation suite that you run locally.

Pytest:

    discovers tests
        ↓
    creates fixtures
        ↓
    starts Playwright
        ↓
    launches Chromium
        ↓
    executes tests
        ↓
    returns an exit status

If Pytest returns a failure status, the GitHub Actions job fails.

---

# 13. Add Playwright Tracing

For better diagnostics:

    - name: Run tests
      run: pytest --browser chromium --tracing=retain-on-failure

The tracing option tells the Playwright Pytest integration to retain traces when tests fail.

A trace can make browser failures much easier to investigate.

---

# 14. Upload Test Results

Use:

    - name: Upload Playwright test results
      if: ${{ !cancelled() }}
      uses: actions/upload-artifact@v6
      with:
        name: playwright-test-results
        path: test-results/
        retention-days: 30

What the fields mean:

| Field | Purpose |
|---|---|
| if | Controls whether this step executes. |
| uses | Uses GitHub's artifact upload action. |
| with.name | Name displayed for the uploaded artifact. |
| with.path | Directory to upload. |
| retention-days | How long GitHub retains the artifact. |

This is useful for:

    screenshots
    traces
    failure diagnostics

---

# 15. Complete Reference Workflow

A modern reference workflow for this repository is:

    name: Playwright Tests

    on:
      push:
        branches: ["main"]
      pull_request:
        branches: ["main"]

    jobs:
      test:
        # Stop a runaway CI job after 60 minutes.
        timeout-minutes: 60

        # Use a GitHub-hosted Linux runner.
        runs-on: ubuntu-latest

        steps:
          # Download the repository onto the runner.
          - name: Checkout repository
            uses: actions/checkout@v6

          # Install the project's Python runtime.
          - name: Set up Python
            uses: actions/setup-python@v6
            with:
              python-version: "3.13"

          # Install the Python packages required by the test framework.
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt

          # Install Chromium and its Linux system dependencies.
          - name: Install Playwright browsers and dependencies
            run: python -m playwright install --with-deps chromium

          # Run the complete Playwright test suite.
          - name: Run tests
            run: pytest --browser chromium --tracing=retain-on-failure

          # Preserve test diagnostics.
          - name: Upload Playwright test results
            if: ${{ !cancelled() }}
            uses: actions/upload-artifact@v6
            with:
              name: playwright-test-results
              path: test-results/
              retention-days: 30

---

# 16. How To Create It Manually

## Step 1 — Create the workflow directory

Linux/macOS/Git Bash:

    mkdir -p .github/workflows

PowerShell:

    New-Item -ItemType Directory -Force .github/workflows

## Step 2 — Create the YAML file

Create:

    .github/workflows/tests.yml

## Step 3 — Start with the name

    name: Playwright Tests

## Step 4 — Add triggers

    on:
      push:
        branches: ["main"]
      pull_request:
        branches: ["main"]

## Step 5 — Add the job

    jobs:
      test:
        timeout-minutes: 60
        runs-on: ubuntu-latest

## Step 6 — Add steps

Add them in this order:

    checkout
    Python
    dependencies
    Playwright browser/dependencies
    pytest
    artifacts

The order matters because each step prepares the environment for the next one.

For the current repository, the production workflow order is:

    checkout
    Python + pip cache
    Node.js
    Python dependencies
    Playwright + Chromium dependencies
    Allure CLI
    pytest
    Allure report
    artifact upload

---

# 17. Commit the Workflow

After saving the file:

    git status

Inspect the YAML:

    git diff -- .github/workflows/tests.yml

Stage it:

    git add .github/workflows/tests.yml

Commit it:

    git commit -m "ci: add Playwright GitHub Actions workflow"

Push it:

    git push origin main

---

# 18. Watch the Workflow

On GitHub:

    Repository
        ↓
    Actions
        ↓
    Playwright Tests
        ↓
    Latest workflow run

You can inspect each step:

    Checkout repository
    Set up Python
    Install dependencies
    Install Playwright browsers and dependencies
    Run tests
    Upload Playwright test results

---

# 19. How To Diagnose CI Failures

## Failure during checkout

Investigate:

    repository permissions
    branch/ref configuration
    action syntax

## Failure during Python setup

Investigate:

    Python version
    setup-python action
    runner configuration

## Failure during dependency installation

Investigate:

    requirements.txt
    package versions
    Python compatibility

## Failure during Playwright installation

Investigate:

    browser installation
    Linux system dependencies
    Playwright version

## Failure during pytest

Investigate:

    test traceback
    fixture errors
    Playwright errors
    screenshots
    traces
    application behavior

---

# 20. Secrets

Never commit:

    passwords
    API tokens
    private keys
    production credentials

Use GitHub repository/environment secrets for real credentials.

The local learning application currently uses non-sensitive demo credentials, so secrets are not required yet.

---

# 21. CI Progression For This Repository

### Level 1 — Basic CI

    checkout
       ↓
    Python
       ↓
    dependencies
       ↓
    Playwright
       ↓
    pytest

### Level 2 — Diagnostics

    pytest
       ↓
    trace on failure
       ↓
    upload artifacts

### Level 3 — Parallel execution

    CI
     ↓
    multiple workers
     ↓
    faster feedback

### Level 4 — Quality gates

    lint
     ↓
    API tests
     ↓
    UI tests
     ↓
    artifacts
     ↓
    pass/fail gate

### Level 5 — Real application

    application deployment
           ↓
    Playwright E2E tests
           ↓
    report
           ↓
    deployment quality signal

---

# 22. Local vs CI

Local command:

    pytest --browser chromium

CI command:

    pytest --browser chromium

The test intent should remain the same.

The major difference is the execution environment:

    Local developer environment
            versus
    Clean GitHub-hosted runner

---

## Official References

Playwright Python CI:
https://playwright.dev/python/docs/ci

Playwright Python CI setup:
https://playwright.dev/python/docs/ci-intro

GitHub Actions:
https://docs.github.com/actions


---

# 23. Current CI Verification

The repository has a verified successful GitHub Actions run using the current Playwright workflow.

Result:

    7 passed

The successful job also completed:
- Allure report generation
- Allure report artifact upload
- test evidence artifact upload

The workflow is therefore no longer only a configuration exercise; it has been executed successfully on a clean GitHub-hosted runner.