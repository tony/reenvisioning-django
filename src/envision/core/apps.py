"""Kudos: https://github.com/strawberry-graphql/strawberry-django/blob/b8fa1c1/examples/django/app/apps.py"""

from django.apps import AppConfig


class ExampleAppConfig(AppConfig):
    name = "app"
    verbose_name = "Example App"
