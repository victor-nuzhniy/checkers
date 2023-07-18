"""Module for models 'play' app."""
from django.contrib.auth.models import User
from django.db import models


class Result(models.Model):
    """Model for storing user ratings."""

    player = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Player")
    rival = models.CharField(max_length=100, verbose_name="Rival name")
    count = models.IntegerField(verbose_name="Count")

    def __str__(self):
        """Represent model instance."""
        return f"{self.player}-{self.rival}-{self.count}"
