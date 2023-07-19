"""Consumers for 'play' app."""
import json
from typing import List

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User

from play.models import Result


class PlayConsumer(WebsocketConsumer):
    """Class socket server for playing page."""

    def connect(self) -> None:
        self.play_name = self.scope["url_route"]["kwargs"]["player_name"]
        self.play_group_name = "play_%s" % self.play_name
        async_to_sync(self.channel_layer.group_add)(
            self.play_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.play_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.play_group_name, {"type": "play_message", "message": message}
        )
        # self.send(text_data=json.dumps({"message": message}))

    def play_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))


class StartConsumer(WebsocketConsumer):
    """Class socket server for start page."""

    def connect(self) -> None:
        self.play_name = "start"
        self.play_group_name = "page_%s" % self.play_name
        async_to_sync(self.channel_layer.group_add)(
            self.play_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.play_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        if message.get("type") == "game_over":
            winner: User = User.objects.get(id=message.get("winner"))
            loser: User = User.objects.get(id=message.get("loser"))
            Result.objects.bulk_create([
                Result(player=winner, rival=loser.username, count=2),
                Result(player=loser, rival=winner.username, count=0),
            ])
        async_to_sync(self.channel_layer.group_send)(
            self.play_group_name, {"type": "play_message", "message": message}
        )
        # self.send(text_data=json.dumps({"message": message}))

    def play_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))


class ProposeToPlay(WebsocketConsumer):
    """Class socket server for start page."""

    def connect(self) -> None:
        self.play_name = self.scope["url_route"]["kwargs"]["player_id"]
        self.play_group_name = "proposal_%s" % self.play_name
        async_to_sync(self.channel_layer.group_add)(
            self.play_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.play_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.play_group_name, {"type": "play_message", "message": message}
        )
        # self.send(text_data=json.dumps({"message": message}))

    def play_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
