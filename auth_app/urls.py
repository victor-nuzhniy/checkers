"""Urls for auth_app."""
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from django.urls import path

from auth_app import views

app_name = 'auth_app'

urlpatterns = [
    path(
        'accounts/login/',
        views.CustomLoginView.as_view(),
        name='login',
    ),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path(
        'accounts/password_change/',
        views.CustomPasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'accounts/password_change/done/',
        PasswordChangeDoneView.as_view(template_name='play/password_change_done.html'),
        name='password_change_done',
    ),
    path(
        'accounts/password_reset/',
        views.CustomPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'accounts/password_reset/done',
        PasswordResetDoneView.as_view(template_name='play/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'accounts/reset/done',
        PasswordResetCompleteView.as_view(
            template_name='play/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path('accounts/registration/', views.RegisterView.as_view(), name='registration'),
    path(
        'accounts/email_verification/<uidb64>/<token>',
        views.EmailActivationView.as_view(),
        name='activate',
    ),
    path(
        'accounts/email_confirm/',
        views.RegisterEmailConfirmView.as_view(),
        name='email_confirm',
    ),
]
