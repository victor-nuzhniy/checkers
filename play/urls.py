"""Urls list for 'play' app."""

from django.urls import path, include

from play.views import RegisterView, MainView

app_name = "play"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registration/', RegisterView.as_view(), name='registration'),
    path('', MainView.as_view(), name='main'),
]
