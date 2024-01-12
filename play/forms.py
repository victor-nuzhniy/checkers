"""Forms for 'play' app."""
from typing import Any

from django import forms
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    """Form class for change user data."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        fields = self.fields
        fields['username'].widget.attrs['class'] = 'custom-input custom-input-height'
        fields['email'].widget.attrs['class'] = 'custom-input custom-input-height'
        fields['first_name'].widget.attrs['class'] = 'custom-input custom-input-height'
        fields['last_name'].widget.attrs['class'] = 'custom-input custom-input-height'

    class Meta:  # noqa WPS306
        """Class Meta for UserProfileForm."""

        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ResultDeleteForm(forms.Form):
    """Form class for delete result instance."""

    id = forms.IntegerField(widget=forms.HiddenInput())
