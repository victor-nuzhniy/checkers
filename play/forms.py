"""Forms for 'play' app."""
from typing import Any

from django import forms
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    """Form class for change user data."""

    class Meta:
        """Class Meta for UserProfileForm."""
        model = User
        fields = ("username", "email")


class ResultDeleteForm(forms.Form):
    """Form class for delete result instance."""

    id = forms.IntegerField(widget=forms.HiddenInput())
