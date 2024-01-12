"""Module with configuration for auth_app."""
from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Class with configuration for auth_app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app'
