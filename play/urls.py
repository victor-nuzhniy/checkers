"""Urls list for 'play' app."""
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from django.urls import path

from play.views import (
    AccountUpdateView,
    CustomLoginView,
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    EmailActivationView,
    EntryView,
    MainView,
    ProfileView,
    RatingView,
    RegisterEmailConfirmView,
    RegisterView,
    ResultDeleteView,
    StartView,
)

app_name = "play"

urlpatterns = [
    path(
        "accounts/login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path(
        "accounts/password_change/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="play/registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done",
        PasswordResetDoneView.as_view(
            template_name="play/registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done",
        PasswordResetCompleteView.as_view(
            template_name="play/registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("accounts/registration/", RegisterView.as_view(), name="registration"),
    path(
        "accounts/email_verification/<uidb64>/<token>",
        EmailActivationView.as_view(),
        name="activate",
    ),
    path(
        "accounts/email_confirm/",
        RegisterEmailConfirmView.as_view(),
        name="email_confirm",
    ),
    path("", EntryView.as_view(), name="entry"),
    path("<int:player_pk>/<int:rival_pk>/", MainView.as_view(), name="main"),
    path("start/", StartView.as_view(), name="start"),
    path("rating/", RatingView.as_view(), name="rating"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("account/update/<int:pk>", AccountUpdateView.as_view(), name="account"),
    path("delete-result/<int:pk>/", ResultDeleteView.as_view(), name="delete_result"),
]
