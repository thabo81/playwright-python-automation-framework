# Visual Regression and Accessibility Testing Notes

These notes define the next quality-engineering extensions for the Python + Pytest + Playwright learning framework. They are **documented learning goals, not implemented test capabilities** in the current suite.

## 1. Visual regression testing

Visual regression testing compares a current page or component render with a reviewed baseline image. It can reveal unintended changes in layout, spacing, fonts, colors, responsive behaviour, and component rendering that functional DOM assertions may not detect.

### What to test first

Start with a few stable, high-value targets rather than taking snapshots of every page:

- Login form and validation message.
- Dashboard heading and welcome panel.
- A representative component at desktop and mobile-like viewport sizes.

### Python / Playwright capture example

This example captures a screenshot for inspection. It verifies that a capture file was produced; it does **not** compare the image to a baseline.

```python
from pathlib import Path

from playwright.sync_api import Page, expect


def test_capture_dashboard_screenshot(
    authenticated_page: Page,
    test_app_url: str,
    tmp_path: Path,
) -> None:
    # Use the saved login state so the protected route displays the dashboard.
    authenticated_page.goto(f"{test_app_url}/dashboard")

    # Wait for the main dashboard element instead of sleeping for an arbitrary duration.
    expect(
        authenticated_page.get_by_test_id("dashboard-title")
    ).to_be_visible()

    # Save a full-page screenshot as temporary test evidence.
    screenshot_path = tmp_path / "dashboard.png"
    authenticated_page.screenshot(
        path=str(screenshot_path),
        full_page=True,
        animations="disabled",
    )

    # This assertion checks the capture exists, not visual similarity.
    assert screenshot_path.exists()
```

### Methods Used

- `authenticated_page.goto(...)`: opens a protected page using an authenticated fixture.
- `expect(...).to_be_visible()`: waits for the page element to be visible before capturing.
- `page.screenshot(...)`: saves a screenshot to a file.
- `tmp_path`: Pytest's per-test temporary directory fixture.

### How a real visual-regression check should work

1. **Choose a Python-compatible comparator.** The current repository uses Python + Pytest. Do not copy JavaScript/TypeScript Playwright Test's `expect(page).toHaveScreenshot()` API directly into the Python suite; that built-in screenshot assertion belongs to the Playwright Test runner.
2. **Create and review baselines** in a controlled environment, then store them in a dedicated snapshots/baselines directory.
3. **Make rendering deterministic:** pin browser/OS versions where possible, use a fixed viewport and device scale factor, use stable test data, and wait for images/fonts/content to finish loading.
4. **Manage noise carefully:** disable animations and mask volatile content such as timestamps only when those areas are not the subject of the test.
5. **Review diffs before updating a baseline.** An intentional UI change should be approved; never auto-accept all changed snapshots just to make CI green.
6. **Retain functional checks.** Pixel similarity does not verify navigation, accessibility, form validation, or business behaviour.

### Common failure modes

- Baselines created on a different operating system, browser build, font set, or viewport.
- Dynamic dates, avatars, randomized content, or asynchronous images.
- Capturing before the page reaches the expected state.
- Overly permissive difference thresholds that hide genuine regressions.
- Treating a saved screenshot as a visual comparison test when no comparison has occurred.

## 2. Accessibility testing

Accessibility testing (often shortened to *a11y*) assesses whether people with differing abilities can perceive, understand, navigate, and operate the interface. It should be treated as a combination of automated testing, manual assessment, and, where practical, feedback from users with disabilities.

### Automated scanning option for Python

Playwright's official accessibility guide demonstrates axe using the JavaScript package `@axe-core/playwright`. For a Python + Pytest framework, `axe-playwright-python` is a possible third-party integration. It is a community package, not an official Microsoft Playwright component. Check its current maintenance, version compatibility, dependencies, and result format before adding it to `requirements.txt`.

Illustrative test shape, **after installing and validating the optional package**:

```python
from playwright.sync_api import Page

from axe_playwright_python.sync_playwright import Axe


def test_dashboard_has_no_automated_accessibility_violations(
    authenticated_page: Page,
    test_app_url: str,
) -> None:
    # Open the page in the state that users will actually encounter.
    authenticated_page.goto(f"{test_app_url}/dashboard")

    # Run axe-core rules against the page's current DOM state.
    axe = Axe()
    results = axe.run(authenticated_page)

    # Report the scanner output if any violations are found.
    assert results.violations_count == 0, results.response
```

### Methods Used

- `Axe()`: creates the axe wrapper documented by the package.
- `axe.run(page)`: scans the page in its current state.
- `results.violations_count`: reads the reported count of detected violations in the package's documented usage.
- `assert ... , results.response`: fails with scan details available for investigation.

Validate this example against the exact package version you install. Scan pages after reaching the relevant state; for example, open a menu or validation panel before scanning if that state needs coverage.

### What automated scans can and cannot do

Automated scans can help identify some issues, including:

- Missing or invalid accessible names on controls.
- Some color-contrast failures.
- Invalid ARIA properties or certain semantic-structure issues.
- Duplicate IDs that can confuse assistive technologies.

They cannot reliably detect every accessibility barrier. A zero-violation automated scan does **not** prove full WCAG compliance. Agree the relevant WCAG version and conformance level (for example, WCAG 2.2 AA if appropriate to the project's requirements) with the responsible stakeholders.

### Manual checks to retain

- **Keyboard operation:** complete key workflows without a mouse; ensure controls can be reached and activated.
- **Focus visibility and order:** verify visible focus and logical focus movement, including dialogs and menus.
- **Names and labels:** check buttons, form inputs, instructions, and controls have meaningful accessible names.
- **Validation feedback:** ensure errors are understandable and programmatically associated with the relevant fields.
- **Zoom, reflow, and contrast:** inspect important pages at zoomed and narrower viewport sizes.
- **Screen-reader spot checks:** review meaningful headings, landmarks, control names, state changes, and error announcements.
- **Defect quality:** record the affected page, steps, expected/actual behaviour, impact, relevant WCAG criterion if identified, and retest evidence.

Use automated scans as a repeatable CI safety net, with manual checks for user flows and issues that tools cannot reliably judge.

## 3. Suggested implementation order

1. Choose and document the Python visual-comparison tool; add one baseline test for a stable dashboard region.
2. Run the visual check locally and in CI; document baseline review/update workflow and store failure diffs as artifacts.
3. Evaluate `axe-playwright-python` against the installed Playwright version and local fixture model before adding the dependency.
4. Add automated accessibility scans to selected pages and stable interactive states.
5. Add a short manual accessibility checklist to regression review; track findings as defects.
6. Keep both capabilities separate from ordinary functional assertions so that failures identify whether the issue is behaviour, appearance, or accessibility.

## References

- Playwright Python screenshots: https://playwright.dev/python/docs/screenshots
- Playwright accessibility testing overview: https://playwright.dev/docs/accessibility-testing
- axe-playwright-python on PyPI: https://pypi.org/project/axe-playwright-python/
- axe-playwright-python source repository: https://github.com/pamelafox/axe-playwright-python
