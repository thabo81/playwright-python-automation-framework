# Chapter 16 — Playwright Interview Preparation

**Source alignment:** This guide follows the themes of Chapter 16, *Playwright Cheat Sheet and Interview Questions*, in *Web Automation with Playwright and Python using AI and MCP* by Kailash Pathak. It expands the chapter's revision topics into an original study bank. The answers are paraphrased learning explanations, not a reproduction of the book's wording.

The difficulty levels represent the depth of reasoning expected, not a guarantee of how a particular employer will label a question. The guide avoids code snippets so the focus stays on explaining concepts and engineering decisions.

## How to answer an interview question

For most technical questions, use four steps:

1. **Define it:** state what the concept is.
2. **Explain the purpose:** describe the problem it solves.
3. **Apply it:** give a realistic testing example.
4. **Mention a limitation or trade-off:** show that you understand when it may not be enough.

---

## Easy — Core concepts

### 1. What is Playwright, and what is it used for?

**Answer:** Playwright is a browser automation framework used to interact with web applications and verify their behaviour. It supports Chromium, Firefox, and WebKit browser engines and can help with UI workflows, cross-browser checks, and related automation tasks. It is useful for repeating important user journeys and detecting regressions after application changes.

**Interview point:** Explain it as a way to automate and verify browser behaviour, not simply as a tool that clicks buttons.

### 2. Why use Python with Playwright?

**Answer:** Python provides readable syntax and a broad ecosystem for test utilities, data handling, API clients, and reporting integrations. Combined with Playwright, it lets a QA engineer express browser interactions and checks in a language that is approachable and maintainable. The choice still depends on the team's skills, existing stack, and project needs.

### 3. What is the difference between a browser, a browser context, and a page?

**Answer:**
- A **browser** is the running browser instance or engine.
- A **browser context** is an isolated session inside that browser, with its own session data such as cookies and storage.
- A **page** is an individual tab or page within a context.

Contexts are important because tests can use separate sessions without unintentionally sharing login state or other browser data. A context can contain more than one page.

### 4. What is a locator, and why does locator quality matter?

**Answer:** A locator identifies an element that the test needs to interact with or inspect. A reliable locator describes the intended element clearly and remains stable when the interface changes. Locators based on accessible roles, names, labels, or stable attributes often communicate intent better than selectors that depend on layout or element position.

**Common weak answer:** “A locator is just an ID or XPath.” Locators can use several strategies, and the important question is whether the chosen strategy is clear and reliable.

### 5. What is auto-waiting, and why is it useful?

**Answer:** Web applications update asynchronously. Auto-waiting helps Playwright wait for relevant actionability conditions before performing supported actions, which reduces failures caused by trying to interact with elements too early. It does not mean that every application condition or business outcome will be waited for automatically. Tests still need meaningful assertions and appropriate synchronization around application behaviour.

### 6. What is an assertion in automated testing?

**Answer:** An assertion compares observed behaviour with an expected result. It turns a sequence of browser actions into a test by deciding whether the required condition was satisfied. For example, after a user logs in, the test should verify evidence of the expected authenticated state rather than assuming success because the submit action completed.

---

## Medium — Framework design and dependable tests

### 7. How would you choose reliable locators for a login page?

**Answer:** I would start with selectors that express user-visible meaning, such as the accessible name or role of a button and the label associated with an input. If that is not practical, I would ask the development team for stable test attributes. I would avoid relying on styling classes, deeply nested page structure, or positional selection unless the position is itself part of the requirement. Finally, I would verify that the locator identifies the intended element uniquely and behaves consistently.

### 8. What is the Page Object Model, and what problem does it solve?

**Answer:** The Page Object Model organizes page-specific interaction details separately from the tests that describe scenarios. A page object can group locators and common page actions so tests do not repeatedly implement the same interaction details. When the page changes, the affected page object can often be updated in one place.

**Trade-off:** Overly large page objects or excessive layers of abstraction can make tests harder to follow. The goal is clear ownership and useful reuse, not abstraction for its own sake.

### 9. What is a Pytest fixture, and why is it useful in a Playwright framework?

**Answer:** A fixture provides reusable setup or resources to tests and can also manage cleanup. Examples include preparing browser resources, creating test data, or establishing a known precondition. Fixtures help avoid duplicated setup and clarify what a test depends on.

**Important distinction:** Shared setup should not create hidden coupling between tests. A fixture's scope and cleanup must fit the resource and isolation requirements.

### 10. How would you investigate a flaky test?

**Answer:** First I would establish whether the failure is intermittent and collect the error message, trace, screenshot, logs, and relevant CI information. Then I would determine whether the problem is caused by timing, an unstable locator, shared state, test data, network dependency, environment variation, or a genuine product defect. I would reproduce it where practical, fix the underlying cause, and rerun both the affected test and relevant regression coverage.

**Avoid:** Adding arbitrary sleeps or repeating the test until it passes without understanding the cause.

### 11. When would you use API testing alongside UI testing?

**Answer:** API tests are useful for checking service contracts, status codes, response content, validation, and business rules without going through the whole interface. UI tests verify that the user can complete a workflow and that the interface integrates with the services correctly. API operations can also help prepare test state when that is appropriate and safe. I would use UI tests for critical user journeys and place lower-level checks at the API or service level when they offer faster, clearer feedback.

### 12. Why and when would you mock an API response?

**Answer:** Mocking lets a test control a dependency's response so the test can focus on a defined scenario. It is useful for predictable edge cases, error responses, empty states, or responses that are difficult to reproduce on demand. Mocked tests can be stable and fast, but they do not prove that the real service is correct. I would retain complementary tests against the real service or a suitable integration environment.

### 13. Why is browser-context isolation important when tests run in parallel?

**Answer:** Parallel tests can interfere if they share cookies, authentication state, local storage, mutable data, or other resources. Independent contexts help separate browser sessions, making each test's starting state more predictable. Context isolation alone does not isolate shared backend records or external systems, so test data and cleanup must also be designed for parallel execution.

### 14. How do reports and debugging artifacts improve a test framework?

**Answer:** Reports summarize what passed and failed, while supporting artifacts provide evidence for investigation. A useful failure record can include the error, execution history, screenshot, trace, logs, and relevant environment details. This reduces the time spent reproducing a failure and helps teams distinguish product defects from test or infrastructure problems.

**Trade-off:** Artifacts should avoid exposing credentials, tokens, personal data, or other sensitive information.

---

## Hard — Architecture, delivery, and engineering judgment

### 15. A test passes locally but fails in GitHub Actions. How would you approach it?

**Answer:** I would compare the local and CI environments before changing the test. I would examine browser and dependency versions, environment variables, base URL, test data, secrets, permissions, timeouts, network access, working directory, and any difference in execution mode or concurrency. I would inspect the CI trace, screenshot, logs, and reports to identify the failing step. If parallel execution is involved, I would check for shared state and order dependencies. After finding the cause, I would fix the environment or test design, then verify the result with the affected test and the full relevant suite.

**Why this is hard:** It requires a structured diagnosis across test code, application state, infrastructure, and pipeline configuration.

### 16. How would you decide which tests to run in the UI, API, visual, or accessibility layer?

**Answer:** I would start with the risk and the claim that needs to be verified. API checks are efficient for service rules and data contracts. UI tests are appropriate for critical user journeys and integration behaviour. Visual comparisons can reveal unintended appearance changes. Accessibility checks can identify many detectable barriers, with human evaluation still needed for broader usability. I would avoid duplicating every rule at every layer and instead build complementary coverage that provides clear evidence at reasonable maintenance cost.

### 17. How would you design a maintainable automation framework for a growing product?

**Answer:** I would keep test intent readable, centralize repeated page-specific behaviour where it is useful, and provide clear fixture and test-data conventions. I would define how tests are categorized, how configuration is managed, how failures are reported, and how evidence is retained. CI should run a dependable set of checks on changes and support broader coverage where appropriate. I would add abstractions only when they reduce duplication or clarify a stable concept, and I would periodically remove abstractions that obscure behaviour.

**Signals of a strong answer:** clear boundaries, isolation, controlled configuration, useful diagnostics, and an explicit maintenance strategy.

### 18. How can visual regression tests produce false alarms, and how should baselines be managed?

**Answer:** Screenshots can differ because of dynamic data, animation, timestamps, fonts, browser versions, viewport size, rendering differences, or legitimate interface changes. I would standardize the environment and use stable test data where possible, then review the actual screenshot and difference image. Baseline updates should be deliberate, tied to an understood product change, and reviewed like other test changes. Automatically approving all new output would risk hiding regressions.

### 19. What are the limitations of automated accessibility testing?

**Answer:** Automated checks can detect many rule-based issues, such as some missing names, invalid attributes, or contrast problems. They cannot reliably assess every user journey, whether content is understandable, whether keyboard navigation feels logical, or how a person using assistive technology experiences a workflow. I would combine automated scanning with keyboard testing, manual checks, and relevant assistive-technology evaluation. Passing an automated scan should not be presented as proof of full accessibility compliance.

### 20. AI proposes a “self-healing” locator that makes a failing test pass. Should you accept it?

**Answer:** Not without reviewing the intended behaviour and the evidence. The original failure may reflect a harmless selector change, but it may also indicate a removed control, a changed workflow, or a regression. I would confirm that the new locator uniquely identifies the intended element, review what changed, and rerun related tests. A repair is acceptable only if it preserves the test's purpose and does not weaken the assertion or skip the requirement.

### 21. What does MCP add to an AI-assisted Playwright workflow?

**Answer:** MCP provides a structured way for an AI application to access compatible tools and context. In an automation workflow, a Playwright MCP server can expose browser interaction capabilities so the AI can work with the current page and tool results rather than relying only on a text description. The AI may use those results to plan its next step, but this does not guarantee correct decisions or replace explicit test assertions.

**Security and control:** Tool permissions, allowed actions, sensitive data, and human review must be considered before using an agent against real systems.

### 22. How would you evaluate whether AI is improving your test automation process?

**Answer:** I would measure outcomes rather than counting generated tests. Useful measures include time to create and review tests, maintenance effort, flaky-test rate, defect detection, failure diagnosis time, false positives, coverage of important risks, and the impact of changes to the generated tests. I would review a sample of AI-generated changes for correctness and security. If the tool increases test volume but weakens assertions or raises false alarms, it has not improved quality.

### 23. What is the relationship between parallel execution and test reliability?

**Answer:** Parallel execution can shorten feedback time by distributing work, but it increases the importance of isolation and controlled shared resources. Tests that rely on execution order, fixed shared accounts, mutable common records, or global state may fail only when run concurrently. I would make tests independent, isolate browser sessions, allocate unique data where necessary, and only then tune the level of concurrency. If concurrency reveals a race condition, simply reducing concurrency may hide the underlying design issue rather than solve it.

### 24. What role should a human tester retain in an AI-assisted automation framework?

**Answer:** The tester remains responsible for selecting risks, understanding requirements, defining expected behaviour, reviewing generated tests, interpreting failures, and deciding whether evidence is sufficient for release. AI can support ideation, drafting, tool interaction, and investigation, but may make incorrect assumptions or propose changes that weaken coverage. Human oversight is particularly important for high-impact workflows, sensitive data, destructive actions, and ambiguous requirements.

---

## Rapid revision checklist

Before an interview, make sure you can explain these ideas clearly without reading the answers:

- [ ] What Playwright does and why teams use it.
- [ ] The roles of browser, context, and page.
- [ ] How locator choice, synchronization, and assertions affect reliability.
- [ ] The purpose and trade-offs of the Page Object Model.
- [ ] How fixtures support setup, cleanup, and independence.
- [ ] How to investigate a flaky test or a local-versus-CI failure.
- [ ] The different purposes of UI, API, visual, and accessibility tests.
- [ ] How mocking helps and what it does not prove.
- [ ] Why parallel execution requires isolation.
- [ ] How reports and traces support evidence-based debugging.
- [ ] Why visual baselines need review and governance.
- [ ] Why automated accessibility scans are not a complete assessment.
- [ ] How AI-assisted testing and MCP can help, and why human review remains necessary.

## How to practise

1. Answer each question aloud before reading its model answer.
2. Use a real example from this repository where possible.
3. Explain the trade-off, not just the definition.
4. For hard questions, describe the order in which you would investigate the problem.
5. Revisit any answer that you can recognize when reading but cannot explain in your own words.

## Final interview principle

A strong answer connects a concept to a testing risk, explains how the concept addresses that risk, and acknowledges what it cannot guarantee. That demonstrates engineering judgment rather than command memorization.
