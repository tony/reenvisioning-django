"""Integration tests for the core app."""

import json
from typing import Any

import pytest
from django.test import Client
from django.urls import reverse

from envision.core.models import Color, Fruit


@pytest.mark.django_db
class TestGraphQLEndpoints:
    """Test GraphQL endpoints availability."""

    def test_graphql_async_endpoint(self, client: Client) -> None:
        """Test that async GraphQL endpoint is accessible."""
        # Test with POST
        response = client.post(
            "/graphql",
            data='{"query": "{ __typename }"}',
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["__typename"] == "Query"

    def test_graphql_sync_endpoint(self, client: Client) -> None:
        """Test that sync GraphQL endpoint is accessible."""
        response = client.post(
            "/graphql/sync",
            data='{"query": "{ __typename }"}',
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["__typename"] == "Query"

    def test_graphql_introspection(self, client: Client) -> None:
        """Test GraphQL introspection query."""
        query = """
            query {
                __schema {
                    queryType {
                        name
                    }
                    mutationType {
                        name
                    }
                    types {
                        name
                        kind
                    }
                }
            }
        """
        response = client.post(
            "/graphql",
            data=f'{{"query": "{query.replace(chr(10), " ")}"}}',
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()

        assert "errors" not in data
        assert data["data"]["__schema"]["queryType"]["name"] == "Query"
        assert data["data"]["__schema"]["mutationType"]["name"] == "Mutation"

        type_names = {t["name"] for t in data["data"]["__schema"]["types"]}
        assert "Fruit" in type_names
        assert "Color" in type_names
        assert "User" in type_names


@pytest.mark.django_db
class TestFullWorkflow:
    """Test complete workflows through the application."""

    def test_create_and_query_fruit_workflow(self, client: Client) -> None:
        """Test creating a color and fruit, then querying them."""
        # Create a color
        create_color_mutation = """
            mutation {
                createColor(data: {name: "yellow"}) {
                    id
                    name
                }
            }
        """
        response = client.post(
            "/graphql",
            data=json.dumps({"query": create_color_mutation}),
            content_type="application/json",
        )
        assert response.status_code == 200
        color_data = response.json()["data"]["createColor"]

        # Get the color ID from previous response
        yellow_color = Color.objects.get(name="yellow")

        # Create a fruit with that color
        create_fruit_mutation = f"""
            mutation {{
                createFruit(data: {{name: "lemon", color: {{set: {yellow_color.id}}}}}) {{
                    name
                    color {{
                        name
                    }}
                }}
            }}
        """
        response = client.post(
            "/graphql",
            data=json.dumps({"query": create_fruit_mutation}),
            content_type="application/json",
        )
        assert response.status_code == 200
        fruit_data = response.json()["data"]["createFruit"]
        assert fruit_data["name"] == "lemon"

        # Query all fruits
        query_fruits = """
            query {
                fruits {
                    name
                    color {
                        name
                    }
                }
            }
        """
        response = client.post(
            "/graphql",
            data=json.dumps({"query": query_fruits}),
            content_type="application/json",
        )
        assert response.status_code == 200
        fruits = response.json()["data"]["fruits"]

        lemon = next((f for f in fruits if f["name"] == "lemon"), None)
        assert lemon is not None
        assert lemon["color"]["name"] == "yellow"

    def test_user_registration_workflow(self, client: Client) -> None:
        """Test user registration through GraphQL."""
        register_mutation = """
            mutation {
                register(data: {username: "testuser", email: "test@test.com", password: "SecurePass123!"}) {
                    id
                    username
                    email
                }
            }
        """
        response = client.post(
            "/graphql",
            data=json.dumps({"query": register_mutation}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["register"] is not None
        user_data = data["data"]["register"]
        assert user_data["username"] == "testuser"
        assert user_data["email"] == "test@test.com"