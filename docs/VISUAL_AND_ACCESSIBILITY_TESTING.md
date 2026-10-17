# Visual Regression and Accessibility Testing

This guide documents the implemented dashboard visual-regression and automated accessibility checks, along with their limitations and the manual review practices that should accompany them. The project uses Python + Pytest + Playwright.

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

### Implemented visual-regression check

1. The test is in `tests/visual/test_dashboard_visual.py`; its approved baseline is `tests/visual_baselines/dashboard.png`.
2. The test fixes the viewport at 1280 × 720, waits for dashboard content, disables animations, and captures the `main` region.
3. Pillow compares the current screenshot with the baseline. Pixels with a grayscale difference above 30 are counted, and the test fails when more than 0.2% of pixels exceed that threshold.
4. On a mismatch, the test writes `dashboard-actual.png` and `dashboard-diff.png` under `test-results/visual-diff/`. The CI workflow uploads `test-results/` even when tests fail.
5. Baselines must be deliberately reviewed and updated in the same browser/OS environment used by CI. Never auto-accept a changed baseline merely to make CI green.
6. After an intentional UI change, regenerate the dashboard baseline explicitly with `pytest tests/visual/test_dashboard_visual.py --browser chromium --update-visual-baselines`. The test will skip after writing the file; inspect the image and commit it only after review. Do not pass this option in CI.
6. This is a focused demonstration for the stable dashboard main region, not comprehensive coverage of every page, browser, or viewport. Pixel comparison complements functional assertions; it does not replace them.

### Common failure modes

- Baselines created on a different operating system, browser build, font set, or viewport.
- Dynamic dates, avatars, randomized content, or asynchronous images.
- Capturing before the page reaches the expected state.
- Overly permissive difference thresholds that hide genuine regressions.
- Treating a saved screenshot as a visual comparison test when no comparison has occurred.

## 2. Accessibility testing

Accessibility testing (often shortened to *a11y*) assesses whether people with differing abilities can perceive, understand, navigate, and operate the interface. It should be treated as a combination of automated testing, manual assessment, and, where practical, feedback from users with disabilities.

### Implemented automated scan for Python

The test in `tests/accessibility/test_dashboard_accessibility.py` uses `axe-playwright-python==0.1.8` to run axe-core against the authenticated dashboard. This is a third-party community integration, not an official Microsoft Playwright component. The test fails when axe reports violations and includes the scanner response in the failure message.

The implemented test follows this pattern:

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

The dependency is pinned in `requirements.txt`. Scan each relevant page state explicitly; for example, open a menu or validation panel before scanning if that state needs coverage.

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
