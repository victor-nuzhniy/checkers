"""Forms for auth_app."""
from typing import Any

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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        fields = self.fields
        fields['username'].widget.attrs['class'] = 'custom-input custom-input-height'
        fields['email'].widget.attrs['class'] = 'custom-input custom-input-height'
        fields['password1'].widget.attrs['class'] = 'custom-input custom-input-height'
        fields['password2'].widget.attrs['class'] = 'custom-input custom-input-height'

    class Meta:  # noqa WPS306
        """Class Meta for SignupForm."""

        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthForm(AuthenticationForm):
    """Custom authentication form."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        fields = self.fields
        fields['username'].widget.attrs['class'] = 'custom-input custom-input-height'
        fields['password'].widget.attrs['class'] = 'custom-input custom-input-height'


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        fields = self.fields
        fields['old_password'].widget.attrs[
            'class'
        ] = 'custom-input custom-input-height'
        fields['new_password1'].widget.attrs[
            'class'
        ] = 'custom-input custom-input-height'
        fields['new_password2'].widget.attrs[
            'class'
        ] = 'custom-input custom-input-height'


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        fields = self.fields
        fields['email'].widget.attrs['class'] = 'custom-input custom-input-height'


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        fields = self.fields
        fields['new_password1'].widget.attrs[
            'class'
        ] = 'custom-input custom-input-height'
        fields['new_password2'].widget.attrs[
            'class'
        ] = 'custom-input custom-input-height'
