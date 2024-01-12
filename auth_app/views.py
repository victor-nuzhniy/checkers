"""Views class and functions for auth_app."""
import typing

from django import http
from django.contrib.auth import models, tokens, views
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import encoding
from django.utils import http as http_utils
from django.views import generic

from auth_app import forms

account_activation_token = tokens.PasswordResetTokenGenerator()


class RegisterView(generic.FormView):
    """Class for User registration."""

    form_class = forms.SignupForm
    template_name = 'auth_app/register_form.html'
    extra_context = {'title': 'Registration'}
    success_url = reverse_lazy('auth_app:email_confirm')

    def form_valid(
        self,
        form: forms.SignupForm,
    ) -> http.HttpResponseRedirect | http.HttpResponse:
        """Create new user. Add received after creating customer in Zoho CRM zoho_id."""
        user: models.User = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject: str = 'Activate your account'
        message: str = render_to_string(
            'auth_app/email_template.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': http_utils.urlsafe_base64_encode(
                    encoding.force_bytes(user.pk),
                ),
                'token': account_activation_token.make_token(user),
            },
        )
        to_email: str = form.cleaned_data.get('email', '')
        send_mail(
            mail_subject,
            message,
            'admin@email.com',
            [to_email],
            fail_silently=True,
        )
        return super().form_valid(form)


class CustomLoginView(views.LoginView):
    """Custom login view."""

    template_name = 'auth_app/login.html'
    form_class = forms.CustomAuthForm


class CustomPasswordChangeView(views.PasswordChangeView):
    """Custom password change view."""

    template_name = 'auth_app/password_change_form.html'
    form_class = forms.CustomPasswordChangeForm
    success_url = reverse_lazy('auth_app:password_change_done')


class CustomPasswordResetView(views.PasswordResetView):
    """Custom password reset view."""

    template_name = 'auth_app/password_reset_form.html'
    email_template_name = 'auth_app/password_reset_email.html'
    success_url = reverse_lazy('auth_app:password_reset_done')
    form_class = forms.CustomPasswordResetForm


class CustomPasswordResetConfirmView(views.PasswordResetConfirmView):
    """Custom password reset confirm view."""

    template_name = 'auth_app/password_reset_confirm.html'
    form_class = forms.CustomSetPasswordForm
    success_url = reverse_lazy('auth_app:password_reset_complete')


class RegisterEmailConfirmView(generic.TemplateView):
    """Class view for redirection after registration."""

    template_name = 'auth_app/email_confirm.html'
    extra_context = {'title': 'Email confirmation'}


class EmailActivationView(generic.TemplateView):
    """Class view for getting activation info."""

    template_name = 'auth_app/email_activation_result.html'
    extra_context = {'title': 'Email activation'}

    def get_context_data(self, **kwargs: typing.Any) -> dict:
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)
        try:
            uid = encoding.force_str(
                http_utils.urlsafe_base64_decode(self.kwargs.get('uidb64')),
            )
        except (TypeError, ValueError, OverflowError):
            uid = None
        if uid is not None:
            user: typing.Optional[models.User] = models.User.objects.filter(
                pk=uid,
            ).first()
        else:
            user = None
        token = self.kwargs.get('token')
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            message = (
                'Thank you for your email confirmation. Now you can login your account.'
            )
        else:
            message = 'Activation link is not valid!'
        context['message'] = message
        return context
