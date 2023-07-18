"""Consumers for 'play' app."""
import json

from channels.generic.websocket import WebsocketConsumer


class PlayConsumer(WebsocketConsumer):
    """Class."""

    def connect(self) -> None:
        print("connected")
        self.accept()

    def disconnect(self, code):
        print("disconnected")
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message, "message")

        self.send(text_data=json.dumps({"message": message}))
