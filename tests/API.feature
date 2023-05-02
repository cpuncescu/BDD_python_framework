Feature: API practice

  @API
  Scenario: Use API
    Given profile "Admin"
    And I am using site "https://simple-books-api.glitch.me"
    When I send a GET request to "books"
    Then the response status should be "200"
    And the JSON at path "[0].id" should be 1
    And the JSON at path "[1].name" should be "Just as I Am"