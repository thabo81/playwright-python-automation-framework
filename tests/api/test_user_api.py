import pytest
from playwright.sync_api import APIRequestContext, Playwright


@pytest.mark.api
def test_get_user(playwright: Playwright, test_app_url: str) -> None:
    request: APIRequestContext = playwright.request.new_context()

    try:
        response = request.get(f"{test_app_url}/api/user")

        assert response.ok
        assert response.status == 200

        data = response.json()
        assert data == {"id": 1, "name": "Demo User", "role": "SDET"}
    finally:
        request.dispose()
