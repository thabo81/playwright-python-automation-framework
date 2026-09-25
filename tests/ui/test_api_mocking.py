import pytest
from playwright.sync_api import Page


@pytest.mark.ui
@pytest.mark.api
def test_api_response_can_be_mocked(
    page: Page,
    test_app_url: str,
) -> None:
    page.route(
        "**/api/user",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 99, "name": "Mock User", "role": "Mocked SDET"}',
        ),
    )

    page.goto(test_app_url)

    assert page.get_by_test_id("user-name").inner_text() == "Mock User"
    assert page.get_by_test_id("user-role").inner_text() == "Mocked SDET"
