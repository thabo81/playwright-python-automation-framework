@bdd
Feature: User login

  A user should be able to authenticate with valid credentials.

  @smoke
  Scenario: Successful login redirects to the dashboard
    Given I am on the login page
    When I log in with valid credentials
    Then I should be redirected to the dashboard
