"""Tests for Django models."""

import pytest
from django.db import IntegrityError

from envision.core.models import Color, Fruit


@pytest.mark.django_db
class TestColorModel:
    """Test cases for Color model."""

    def test_create_color(self):
        """Test creating a color instance."""
        color = Color.objects.create(name="green")
        assert color.name == "green"
        assert color.pk is not None

    def test_color_name_required(self):
        """Test that color name is required."""
        color = Color(name=None)
        with pytest.raises(IntegrityError):
            color.save()

    def test_color_fruit_relationship(self, red_color, strawberry, raspberry):
        """Test the reverse relationship from color to fruits."""
        fruits = red_color.fruits.all()
        assert fruits.count() == 2
        assert strawberry in fruits
        assert raspberry in fruits


@pytest.mark.django_db
class TestFruitModel:
    """Test cases for Fruit model."""

    def test_create_fruit_without_color(self):
        """Test creating a fruit without a color."""
        fruit = Fruit.objects.create(name="banana")
        assert fruit.name == "banana"
        assert fruit.color is None

    def test_create_fruit_with_color(self, red_color):
        """Test creating a fruit with a color."""
        fruit = Fruit.objects.create(name="cherry", color=red_color)
        assert fruit.name == "cherry"
        assert fruit.color == red_color

    def test_fruit_name_required(self):
        """Test that fruit name is required."""
        fruit = Fruit(name=None)
        with pytest.raises(IntegrityError):
            fruit.save()

    def test_delete_color_cascades_fruit(self, strawberry, red_color):
        """Test that deleting a color cascades to delete related fruits."""
        assert strawberry.color == red_color
        fruit_id = strawberry.id
        red_color.delete()
        assert not Fruit.objects.filter(id=fruit_id).exists()

    def test_fruit_queryset_with_color(self, strawberry, blueberry, red_color, blue_color):
        """Test querying fruits by color."""
        red_fruits = Fruit.objects.filter(color=red_color)
        blue_fruits = Fruit.objects.filter(color=blue_color)

        assert strawberry in red_fruits
        assert blueberry not in red_fruits
        assert blueberry in blue_fruits
        assert strawberry not in blue_fruits