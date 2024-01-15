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
        'login/',
        views.CustomLoginView.as_view(),
        name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'password_change/',
        views.CustomPasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='auth_app/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'password_reset/',
        views.CustomPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'password_reset/done',
        PasswordResetDoneView.as_view(
            template_name='auth_app/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done',
        PasswordResetCompleteView.as_view(
            template_name='auth_app/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path('registration/', views.RegisterView.as_view(), name='registration'),
    path(
        'email_verification/<uidb64>/<token>',
        views.EmailActivationView.as_view(),
        name='activate',
    ),
    path(
        'email_confirm/',
        views.RegisterEmailConfirmView.as_view(),
        name='email_confirm',
    ),
]
