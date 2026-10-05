# Playwright & Pytest Method Reference

This document is the learning reference for the automation framework. It records methods already used in the repository and the methods planned for later roadmap stages.

The project uses the Playwright Python synchronous API with Pytest.

## 1. Methods Already Used

### Playwright Page API

| Method / property | What it does | Example |
|---|---|---|
| page.goto() | Navigates the browser to a URL. | page.goto(url) |
| page.reload() | Reloads the current page. | page.reload() |
| page.title() | Returns the current document title. | page.title() |
| page.url | Returns the current page URL. | page.url |
| page.get_by_role() | Locates an element by accessible role and name. | page.get_by_role("button", name="Login") |
| page.get_by_label() | Locates a form control using its associated label. | page.get_by_label("Username") |
| page.get_by_test_id() | Locates an element by the test-id attribute. | page.get_by_test_id("dashboard-title") |
| page.wait_for_url() | Waits until the page URL matches a pattern. | page.wait_for_url("**/dashboard") |
| page.route() | Intercepts matching network requests. | page.route("**/api/user", handler) |

### Locator API

| Method | What it does | Example |
|---|---|---|
| locator.fill() | Clears an editable field and enters a value. | username.fill("testuser") |
| locator.click() | Clicks an element after actionability checks. | login_button.click() |
| locator.inner_text() | Returns visible text from the element. | name.inner_text() |

### Playwright Assertions

| Method | What it does | Example |
|---|---|---|
| expect() | Creates a Playwright assertion. | expect(heading) |
| to_have_text() | Verifies expected text. | expect(heading).to_have_text("Dashboard") |
| to_be_visible() | Verifies that an element is visible. | expect(error).to_be_visible() |

### Browser Context and Authentication

| Method | What it does | Example |
|---|---|---|
| browser.new_context() | Creates an isolated browser context. | browser.new_context() |
| context.new_page() | Creates a page inside the context. | context.new_page() |
| context.storage_state() | Saves cookies/local storage for reuse. | context.storage_state(path=state_path) |
| context.close() | Closes the context and its pages. | context.close() |

### API Testing

| Method / property | What it does | Example |
|---|---|---|
| playwright.request.new_context() | Creates an isolated API request context. | playwright.request.new_context() |
| request.get() | Sends a GET request. | request.get("/api/user") |
| response.ok | Indicates whether the response was successful. | assert response.ok |
| response.status | Returns the HTTP status code. | assert response.status == 200 |
| response.json() | Parses a JSON response body. | response.json() |
| request.dispose() | Releases API request-context resources. | request.dispose() |

### API Mocking

The framework has already used page.route() to intercept an API request and route.fulfill() to provide a deterministic mocked response.

| Method | What it does |
|---|---|
| page.route() | Starts request interception for a matching URL pattern. |
| route.fulfill() | Replaces the real response with a mocked response. |

---

## 2. Pytest Features Already Used

| Feature | What it does |
|---|---|
| @pytest.fixture | Creates reusable test setup/dependencies. |
| fixture scope="session" | Keeps a fixture available for the entire test session. |
| yield | Provides a resource to the test and continues with cleanup afterward. |
| @pytest.mark.ui | Categorizes a test as UI automation. |
| @pytest.mark.api | Categorizes a test as API automation. |
| @pytest.mark.smoke | Categorizes a test as a smoke test. |
| pytest.TempPathFactory | Creates temporary directories for test-session artifacts. |

---

# 3. Locator Methods To Learn

Playwright recommends user-facing locators and explicit test contracts such as roles, labels, and test IDs. The locator system is also a core part of Playwright's auto-waiting and retry behavior.

| Method | Purpose |
|---|---|
| page.get_by_text() | Locate an element by visible text. |
| page.get_by_placeholder() | Locate an input by its placeholder text. |
| page.get_by_role() | Locate an element by accessible role and name. |
| page.get_by_label() | Locate a form control through its label. |
| page.get_by_test_id() | Locate using a dedicated automation test ID. |
| page.locator() | Create a locator from a selector. |
| locator.filter() | Narrow a locator based on text or another locator. |
| locator.first | Select the first matching element. |
| locator.nth() | Select an element by zero-based index. |
| locator.count() | Count matching elements. |
| locator.all() | Return locators for currently matched elements. |

## Locator Interaction Methods

| Method | Purpose |
|---|---|
| check() | Checks a checkbox or radio button. |
| uncheck() | Unchecks a checkbox. |
| select_option() | Selects one or more options in a select element. |
| press() | Sends a keyboard key or key combination. |
| press_sequentially() | Types characters sequentially when keyboard events matter. |
| hover() | Moves the mouse over an element. |
| focus() | Gives focus to an element. |
| drag_to() | Drags one element to another. |
| screenshot() | Captures an image of an element. |

---

# 4. Navigation and Waiting

| Method | Purpose | Guidance |
|---|---|---|
| go_back() | Goes back in browser history. | Useful in navigation tests. |
| go_forward() | Goes forward in browser history. | Useful in navigation tests. |
| wait_for_url() | Waits for navigation to a matching URL. | Preferred for URL transitions. |
| wait_for_load_state() | Waits for a selected load state. | Use when a specific load state is meaningful. |
| wait_for_timeout() | Waits a fixed amount of time. | Avoid in normal tests; fixed sleeps can create slow/flaky tests. |

Prefer locators and web-first assertions over arbitrary time delays.

---

# 5. Assertion Methods To Learn

| Assertion | Purpose |
|---|---|
| to_be_visible() | Element is visible. |
| to_be_hidden() | Element is hidden. |
| to_be_enabled() | Element is enabled. |
| to_be_disabled() | Element is disabled. |
| to_have_text() | Element has the expected text. |
| to_contain_text() | Element contains the expected text. |
| to_have_value() | Input has the expected value. |
| to_have_attribute() | Element has an expected attribute/value. |
| to_have_url() | Page has the expected URL. |
| to_have_title() | Page has the expected title. |
| to_have_count() | Locator has the expected number of matches. |

---

# 6. API Testing Methods To Learn

## Request Methods

| Method | HTTP operation |
|---|---|
| request.get() | GET |
| request.post() | POST |
| request.put() | PUT |
| request.patch() | PATCH |
| request.delete() | DELETE |

## Response Inspection

| Method / property | Purpose |
|---|---|
| response.status | HTTP status code. |
| response.ok | Success check. |
| response.json() | Parse JSON response body. |
| response.text() | Read response as text. |
| response.headers | Inspect response headers. |
| response.url | Inspect the final response URL. |

---

# 7. API Mocking and Network Methods To Learn

| Method | Purpose |
|---|---|
| page.route() | Intercept matching network requests. |
| route.fulfill() | Return a controlled mock response. |
| route.continue_() | Continue the original request, optionally with modifications. |
| route.abort() | Abort a request to simulate a network failure. |
| route.fallback() | Pass handling to the next matching route handler. |
| route.request | Access the intercepted request. |
| route.fetch() | Fetch the original request from inside a route handler. |

Typical mocking flow:

    page.route()
        ↓
    inspect request
        ↓
    fulfill / continue / abort

---

# 8. Authentication and Session Methods To Learn

| Method / feature | Purpose |
|---|---|
| context.storage_state() | Save authentication state. |
| browser.new_context(storage_state=...) | Start a fresh authenticated context. |
| context.cookies() | Read current cookies. |
| context.add_cookies() | Add cookies. |
| page.context | Access the page's browser context. |

The repository will use these methods to demonstrate UI login versus reusable authenticated sessions.

---

# 9. Debugging and Diagnostics

| Method / feature | Purpose |
|---|---|
| page.screenshot() | Capture the page as an image. |
| context.tracing.start() | Start Playwright tracing. |
| context.tracing.stop() | Stop tracing and save the trace. |
| page.pause() | Pause execution for interactive debugging. |
| pytest --tracing=retain-on-failure | Retain traces when a test fails. |

These become important during the reporting and troubleshooting phase.

---

# 10. Pytest Features To Learn

| Feature | Purpose |
|---|---|
| @pytest.mark.parametrize | Run one test with multiple datasets. |
| Fixture scope: function | New fixture instance for each test. |
| Fixture scope: class | Shared fixture instance within a test class. |
| Fixture scope: module | Shared fixture instance within a module. |
| Fixture scope: session | Shared fixture instance for the entire run. |
| pytest.skip() | Skip a test at runtime. |
| pytest.importorskip() | Skip when an optional dependency is unavailable. |
| request fixture | Gives fixtures access to test metadata and other fixtures. |
| pytest_addoption() | Adds custom command-line options. |
| pytest_generate_tests() | Generates parametrized tests dynamically. |

---

# 11. Quick Recall

| What are you trying to do? | Start with |
|---|---|
| Find a button | get_by_role() |
| Find a form field | get_by_label() |
| Find a stable automation element | get_by_test_id() |
| Find visible text | get_by_text() |
| Enter data | fill() |
| Click | click() |
| Check checkbox | check() |
| Select dropdown option | select_option() |
| Wait for URL change | wait_for_url() |
| Verify text | expect(...).to_have_text() |
| Verify visibility | expect(...).to_be_visible() |
| Mock an API response | page.route() + route.fulfill() |
| Send an API request | request.get()/post()/put()/patch()/delete() |
| Reuse authentication | storage_state() |
| Save screenshot | page.screenshot() |
| Investigate a failure | tracing + screenshot + CI logs |

---

# 12. Learning Rule

Do not memorize every method before using it.

Use this document as a lookup sheet:

    Identify the testing problem
            ↓
    Find the matching method
            ↓
    Read what it does
            ↓
    Use it in a small test
            ↓
    Refactor into a Page Object or fixture when appropriate

This document should be updated whenever the learning roadmap introduces a significant new Playwright or Pytest API.

## Official Playwright References

https://playwright.dev/python/docs/locators
https://playwright.dev/python/docs/api/class-page
https://playwright.dev/python/docs/api/class-locator
https://playwright.dev/python/docs/ci
