"""Module for creating superuser command on empty db."""
import logging
import os
from typing import Any

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand
from dotenv import load_dotenv

load_dotenv()

logger: logging.Logger = logging.getLogger()


class Command(BaseCommand):
    """Class for initially creating superuser functionality."""

    def handle(self, *args: Any, **options: Any) -> None:  # noqa WPS110
        """Create initial superuser if it had not been created earlier."""
        username: str = os.getenv('DJANGO_SUPERUSER_USERNAME', '')
        email: str = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
        password: str = os.getenv('DJANGO_SUPERUSER_PASSWORD', '')
        if User.objects.count():
            logger.info('Admin account had already been initialized!')
        elif all([username, email, password]):
            logger.info(
                'Creating account for user {username} email {email}'.format(
                    username=username,
                    email=email,
                ),
            )
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
        else:
            raise ImproperlyConfigured('Username, email or passwrod are not set.')
