"""Automated accessibility smoke check for the demo dashboard."""

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page, expect


@pytest.mark.accessibility
@pytest.mark.ui
def test_dashboard_has_no_axe_accessibility_violations(
    authenticated_page: Page,
    test_app_url: str,
) -> None:
    """Scan the rendered dashboard with axe-core and fail on reported violations."""
    # Open the authenticated route so the scan covers the real dashboard state.
    authenticated_page.goto(f"{test_app_url}/dashboard")
    expect(authenticated_page.get_by_test_id("dashboard-title")).to_be_visible()

    # Run axe-core rules against the page's current DOM and accessibility semantics.
    results = Axe().run(authenticated_page)

    # Include the full scanner response in the failure output for triage.
    assert results.violations_count == 0, (
        f"axe-core reported {results.violations_count} accessibility violation(s). "
        f"Scanner response: {results.response}"
    )
