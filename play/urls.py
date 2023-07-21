"""Urls list for 'play' app."""
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from play.views import RegisterView, MainView, StartView, ProfileView, AccountUpdateView, ResultDeleteView, RatingView

app_name = "play"

urlpatterns = [
    path(
        'accounts/login/',
        LoginView.as_view(template_name='play/registration/login.html'),
        name='login',
    ),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='play/registration/password_change_form.html'), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(template_name='play/registration/password_change_done.html'), name='password_change_done'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='play/registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done', PasswordResetDoneView.as_view(template_name='play/registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='play/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done', PasswordResetCompleteView.as_view(template_name='play/registration/password_reset_complete.html'), name='password_reset_done'),
    path('accounts/registration/', RegisterView.as_view(), name='registration'),
    path('<int:player_pk>/<int:rival_pk>/', MainView.as_view(), name='main'),
    path('start/', StartView.as_view(), name="start"),
    path('rating/', RatingView.as_view(), name="rating"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="profile"),
    path('account/update/<int:pk>', AccountUpdateView.as_view(), name="account"),
    path('delete-result/<int:pk>/', ResultDeleteView.as_view(), name="delete_result"),
]
