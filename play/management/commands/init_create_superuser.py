"""Module for creating superuser command on empty db."""
import os
from typing import Any

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    """Class for initially creating superuser functionality."""

    def handle(self, *args: Any, **options: Any) -> None:
        """Create initial superuser if it had not been created earlier."""
        username: str = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email: str = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password: str = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        if not User.objects.count():
            print(f"Creating account for user {username} email {email}")
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
        else:
            print("Admin account had already been initialized!")
