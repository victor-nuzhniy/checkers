"""Urls list for 'play' app."""

from django.urls import path, include

app_name = "play"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]
