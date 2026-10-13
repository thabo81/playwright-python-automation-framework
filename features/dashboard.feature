@bdd
Feature: Authenticated dashboard

  The dashboard should display its title and greet the signed-in user.

  Background:
    Given I am an authenticated user on the dashboard

  @smoke
  Scenario: Dashboard title is displayed
    Then the dashboard title should be displayed

  Scenario: Authenticated user sees a personalized welcome
    Then the dashboard should welcome "Demo User"
