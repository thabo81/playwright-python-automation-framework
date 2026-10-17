"""Dashboard visual regression test using a reviewed screenshot baseline."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image, ImageChops
from playwright.sync_api import Page, expect

# The baseline is committed and reviewed like other source-controlled test data.
BASELINE_PATH = Path(__file__).parents[1] / "visual_baselines" / "dashboard.png"
DIFF_DIRECTORY = Path("test-results") / "visual-diff"

# Ignore tiny antialiasing differences while still detecting meaningful UI changes.
PIXEL_DIFFERENCE_THRESHOLD = 30
MAX_CHANGED_PIXEL_RATIO = 0.002


@pytest.mark.visual
@pytest.mark.ui
def test_dashboard_main_matches_approved_visual_baseline(
    authenticated_page: Page,
    test_app_url: str,
    request: pytest.FixtureRequest,
) -> None:
    """Compare the rendered dashboard main region with the approved baseline."""
    # Fix the viewport so the baseline and current screenshot have matching geometry.
    authenticated_page.set_viewport_size({"width": 1280, "height": 720})
    authenticated_page.goto(f"{test_app_url}/dashboard")

    # Wait for the key content before capturing the region under test.
    expect(authenticated_page.get_by_test_id("dashboard-title")).to_be_visible()
    expect(authenticated_page.get_by_test_id("welcome-message")).to_have_text(
        "Welcome, Demo User"
    )

    # Capture only the main region to avoid comparing irrelevant blank viewport space.
    actual_bytes = authenticated_page.locator("main").screenshot(
        animations="disabled"
    )
    # Downsample the stable main region to reduce antialiasing noise across minor browser builds.
    actual_image = Image.open(BytesIO(actual_bytes)).convert("RGB").resize(
        (632, 57), Image.Resampling.LANCZOS
    )

    # Regeneration is an explicit local action, never an automatic CI fallback.
    if request.config.getoption("--update-visual-baselines"):
        BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        actual_image.save(BASELINE_PATH)
        pytest.skip(
            f"Visual baseline regenerated at {BASELINE_PATH}; review and commit it."
        )

    # Missing baselines are configuration errors; never silently create or accept one.
    assert BASELINE_PATH.is_file(), (
        f"Visual baseline is missing: {BASELINE_PATH}. "
        "Create it deliberately, review it, and commit it before running visual CI."
    )

    with Image.open(BASELINE_PATH) as baseline_file:
        baseline_image = baseline_file.convert("RGB")

    if actual_image.size != baseline_image.size:
        DIFF_DIRECTORY.mkdir(parents=True, exist_ok=True)
        actual_path = DIFF_DIRECTORY / "dashboard-actual.png"
        actual_image.save(actual_path)
        pytest.fail(
            "Dashboard screenshot dimensions changed: "
            f"expected {baseline_image.size}, got {actual_image.size}. "
            f"Actual screenshot: {actual_path}"
        )

    # Calculate the pixel difference and ignore per-pixel changes below the threshold.
    difference = ImageChops.difference(baseline_image, actual_image)
    grayscale_difference = difference.convert("L")
    changed_pixel_mask = grayscale_difference.point(
        lambda value: 255 if value > PIXEL_DIFFERENCE_THRESHOLD else 0
    )
    changed_pixels = changed_pixel_mask.histogram()[255]
    total_pixels = actual_image.width * actual_image.height
    changed_pixel_ratio = changed_pixels / total_pixels

    if changed_pixel_ratio > MAX_CHANGED_PIXEL_RATIO:
        # Keep the actual and highlighted difference images for CI artifact review.
        DIFF_DIRECTORY.mkdir(parents=True, exist_ok=True)
        actual_path = DIFF_DIRECTORY / "dashboard-actual.png"
        diff_path = DIFF_DIRECTORY / "dashboard-diff.png"
        actual_image.save(actual_path)

        # Highlight changed pixels in magenta so reviewers can find the regression.
        highlighted = Image.new("RGB", actual_image.size, (255, 0, 255))
        diff_image = Image.composite(highlighted, actual_image, changed_pixel_mask)
        diff_image.save(diff_path)

        pytest.fail(
            "Dashboard visual regression detected: "
            f"{changed_pixels} of {total_pixels} pixels changed "
            f"({changed_pixel_ratio:.3%}); allowed ratio is "
            f"{MAX_CHANGED_PIXEL_RATIO:.3%}. "
            f"Actual: {actual_path}; diff: {diff_path}"
        )
