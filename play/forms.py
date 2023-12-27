"""Forms for 'play' app."""

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    """Signup form class."""

    def __init__(self, *args, **kwargs):
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["email"].widget.attrs["class"] = "custom-input custom-input-height"
        self.fields["password1"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["password2"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"

    class Meta:
        """Class Meta for SignupForm."""

        model = User
        fields = ("username", "email", "password1", "password2")


class CustomAuthForm(AuthenticationForm):
    """Custom authentication form."""

    def __init__(self, *args, **kwargs):
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["password"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form."""

    def __init__(self, *args, **kwargs):
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["new_password1"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["new_password2"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form."""

    def __init__(self, *args, **kwargs):
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "custom-input custom-input-height"


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form."""

    def __init__(self, *args, **kwargs):
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["new_password2"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"


class UserProfileForm(forms.ModelForm):
    """Form class for change user data."""

    def __init__(self, *args, **kwargs):
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["email"].widget.attrs["class"] = "custom-input custom-input-height"
        self.fields["first_name"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["last_name"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"

    class Meta:
        """Class Meta for UserProfileForm."""

        model = User
        fields = ("username", "email", "first_name", "last_name")


class ResultDeleteForm(forms.Form):
    """Form class for delete result instance."""

    id = forms.IntegerField(widget=forms.HiddenInput())
