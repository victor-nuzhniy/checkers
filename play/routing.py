"""Module for routing 'play' app."""

from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(
        r"ws/(?P<player_name>\w+)/(?P<rival_name>\w+)/$",
        consumers.PlayConsumer.as_asgi(),
    ),
    re_path(
        r"ws/start/(?P<player_name>\w+)/$",
        consumers.StartConsumer.as_asgi(),
    ),
    re_path(
        r"ws/propose/(?P<player_id>\w+)/$",
        consumers.ProposeToPlay.as_asgi(),
    )
]
