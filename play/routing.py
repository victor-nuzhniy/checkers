"""Module for routing 'play' app."""

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/play/(?P<player_id>\w+)/(?P<rival_id>\w+)/$",
        consumers.PlayConsumer.as_asgi(),
    ),
    re_path(
        r"ws/start/(?P<player_id>\w+)/$",
        consumers.StartConsumer.as_asgi(),
    ),
]
