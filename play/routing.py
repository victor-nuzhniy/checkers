"""Module for routing 'play' app."""

from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/", consumers.PlayConsumer.as_asgi()),
]
