"""Tests for GraphQL queries."""

import json

import pytest
from django.test import Client


@pytest.mark.django_db
class TestGraphQLQueries:
    """Test cases for GraphQL queries."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test client and GraphQL endpoint."""
        self.client = Client()
        self.graphql_url = "/graphql"

    def execute_query(self, query, variables=None):
        """Helper method to execute GraphQL query."""
        response = self.client.post(
            self.graphql_url,
            data=json.dumps({"query": query, "variables": variables or {}}),
            content_type="application/json",
        )
        return response.json()

    def test_query_all_fruits(self, strawberry, blueberry, raspberry):
        """Test querying all fruits."""
        query = """
            query {
                fruits {
                    id
                    name
                    color {
                        id
                        name
                    }
                }
            }
        """
        result = self.execute_query(query)

        assert "errors" not in result
        assert "data" in result
        fruits = result["data"]["fruits"]
        assert len(fruits) == 3

        fruit_names = {fruit["name"] for fruit in fruits}
        assert fruit_names == {"strawberry", "blueberry", "raspberry"}

    def test_query_single_fruit(self, strawberry):
        """Test querying a single fruit by ID."""
        query = """
            query GetFruit($pk: ID!) {
                fruit(pk: $pk) {
                    id
                    name
                    color {
                        name
                    }
                }
            }
        """
        result = self.execute_query(query, {"pk": strawberry.id})

        assert "errors" not in result
        assert result["data"]["fruit"]["name"] == "strawberry"
        assert result["data"]["fruit"]["color"]["name"] == "red"

    def test_query_all_colors(self, red_color, blue_color):
        """Test querying all colors."""
        query = """
            query {
                colors {
                    id
                    name
                    fruits {
                        id
                        name
                    }
                }
            }
        """
        result = self.execute_query(query)

        assert "errors" not in result
        assert "data" in result
        colors = result["data"]["colors"]
        assert len(colors) == 2

        color_names = {color["name"] for color in colors}
        assert color_names == {"red", "blue"}

    def test_query_fruits_with_filters(self, strawberry, blueberry, raspberry):
        """Test querying fruits with filters."""
        query = """
            query FruitsByColor($colorName: String!) {
                fruits(filters: {color: {name: {iExact: $colorName}}}) {
                    id
                    name
                }
            }
        """
        result = self.execute_query(query, {"colorName": "red"})

        assert "errors" not in result
        fruits = result["data"]["fruits"]
        assert len(fruits) == 2

        fruit_names = {fruit["name"] for fruit in fruits}
        assert fruit_names == {"strawberry", "raspberry"}

    def test_query_fruits_with_ordering(self, strawberry, blueberry, raspberry):
        """Test querying fruits with ordering."""
        query = """
            query {
                fruits(order: {name: ASC}) {
                    name
                }
            }
        """
        result = self.execute_query(query)

        assert "errors" not in result
        fruits = result["data"]["fruits"]
        fruit_names = [fruit["name"] for fruit in fruits]
        assert fruit_names == ["blueberry", "raspberry", "strawberry"]

    def test_query_fruits_with_pagination(self, strawberry, blueberry, raspberry):
        """Test querying fruits with pagination."""
        # The schema uses cursor-based pagination through strawberry-django
        query = """
            query {
                fruits(pagination: {limit: 2}) {
                    name
                }
            }
        """
        result = self.execute_query(query)

        assert "errors" not in result
        fruits = result["data"]["fruits"]
        assert len(fruits) == 2

    def test_query_nonexistent_fruit(self):
        """Test querying a non-existent fruit."""
        query = """
            query {
                fruit(pk: 99999) {
                    id
                    name
                }
            }
        """
        result = self.execute_query(query)

        # The API throws an error for non-existent items
        assert "errors" in result
        assert "Fruit matching query does not exist" in result["errors"][0]["message"]