"""Kudos: https://github.com/strawberry-graphql/strawberry-django/blob/b8fa1c1/examples/django/app/models.py"""

from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=20)
    color = models.ForeignKey(
        "Color",
        blank=True,
        null=True,
        related_name="fruits",
        on_delete=models.CASCADE,
    )


class Color(models.Model):
    name = models.CharField(max_length=20)
