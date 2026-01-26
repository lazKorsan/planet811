Feature: API Tests
  Background:
    Given I am authenticated as admin

  Scenario: Get all courses
    When I send GET request to "/api/courses"
    Then response status should be 200