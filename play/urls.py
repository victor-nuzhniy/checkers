"""Urls list for 'play' app."""

from django.urls import path, include

from play.views import RegisterView, MainView, StartView

app_name = "play"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registration/', RegisterView.as_view(), name='registration'),
    path('<int:player_pk>/<int:rival_pk>/', MainView.as_view(), name='main'),
    path('start/', StartView.as_view(), name="start"),
]
