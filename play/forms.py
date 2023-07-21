"""Forms for 'play' app."""

from django import forms
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    """Form class for change user data."""

    class Meta:
        """Class Meta for UserProfileForm."""

        model = User
        fields = ("username", "email", "first_name", "last_name")


class ResultDeleteForm(forms.Form):
    """Form class for delete result instance."""

    id = forms.IntegerField(widget=forms.HiddenInput())
