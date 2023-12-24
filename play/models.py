"""Module for models 'play' app."""
from django.contrib.auth.models import User
from django.db import models


class Result(models.Model):
    """Model for storing user ratings."""

    player = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Player")
    rival = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="Rival name"
    )
    count = models.IntegerField(verbose_name="Count")
    created_at = models.DateField(auto_now_add=True, verbose_name="Created at")

    def __str__(self) -> str:
        """Represent model instance."""
        return f"{self.player}-{self.rival}-{self.count}"
