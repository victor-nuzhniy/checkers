"""Consumers for 'play' app."""
import json

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class PlayConsumer(WebsocketConsumer):
    """Class."""

    def connect(self) -> None:
        self.play_name = self.scope["url_route"]["kwargs"]["player_name"]
        print("connect", self.play_name, self.scope)
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
        self.send(text_data=json.dumps({"message": message}))

    def play_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
