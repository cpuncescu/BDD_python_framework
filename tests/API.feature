Feature: API practice

  @API
  Scenario: Use API
    Given profile "Admin"
    And I am using site "https://simple-books-api.glitch.me"
    When I send a GET request to "books"
    Then the response status should be "200"
    And the JSON should be
    """
    [{
    "id": 1,
    "name": "The Russian",
    "type": "fiction",
    "available": true
    },
    {
    "id": 2,
    "name": "Just as I Am",
    "type": "non-fiction",
    "available": false
    },
    {
    "id": 3,
    "name": "The Vanishing Half",
    "type": "fiction",
    "available": true
    },
    {
    "id": 4,
    "name": "The Midnight Library",
    "type": "fiction",
    "available": true
    },
    {
    "id": 5,
    "name": "Untamed",
    "type": "non-fiction",
    "available": true
    },
    {
    "id": 6,
    "name": "Viscount Who Loved Me",
    "type": "fiction",
    "available": true
    }]
    """
    And the JSON at path "[0].id" should be 1
    And the JSON at path "[1].name" should be "Just as I Am"
    And the JSON at path "[1]" should be:
    """
    {"id": 2, "name": "Just as I Am", "type": "non-fiction", "available": false}
    """
    And the JSON has schema "${profile_schema1}"

