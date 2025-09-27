"""Pytest configuration and fixtures for core app tests."""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.test import Client

from envision.core.models import Color, Fruit


@pytest.fixture
def client() -> Client:
    """Return a Django test client."""
    return Client()


@pytest.fixture
def user(db: None) -> AbstractBaseUser:
    """Create and return a test user."""
    User = get_user_model()
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def red_color(db: None) -> Color:
    """Create and return a red color."""
    return Color.objects.create(name="red")


@pytest.fixture
def blue_color(db: None) -> Color:
    """Create and return a blue color."""
    return Color.objects.create(name="blue")


@pytest.fixture
def strawberry(db: None, red_color: Color) -> Fruit:
    """Create and return a strawberry fruit."""
    return Fruit.objects.create(name="strawberry", color=red_color)


@pytest.fixture
def blueberry(db: None, blue_color: Color) -> Fruit:
    """Create and return a blueberry fruit."""
    return Fruit.objects.create(name="blueberry", color=blue_color)


@pytest.fixture
def raspberry(db: None, red_color: Color) -> Fruit:
    """Create and return a raspberry fruit."""
    return Fruit.objects.create(name="raspberry", color=red_color)