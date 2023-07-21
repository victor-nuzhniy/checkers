"""Consumers for 'play' app."""
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from play.models import Result


class PlayConsumer(WebsocketConsumer):
    """Class socket server for playing page."""

    def __init__(self, *args, **kwargs) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.play_group_name = None
        self.player_id = None
        self.rival_id = None
        self.player_id = None

    def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.rival_id = self.scope["url_route"]["kwargs"]["rival_id"]
        self.play_group_name = f"play_{self.player_id}_{self.rival_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.play_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        """Disconnect group from channel layer."""
        async_to_sync(self.channel_layer.group_discard)(
            self.play_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """Receive and process messages."""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.play_group_name, {"type": "play_message", "message": message}
        )

    def play_message(self, event):
        """Send message."""
        self.send(text_data=json.dumps(event))


class StartConsumer(WebsocketConsumer):
    """Class socket server for start page."""

    def __init__(self, *args, **kwargs) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.start_name = None
        self.start_group_name = None

    def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.start_name = self.scope["url_route"]["kwargs"]["player_id"]
        self.start_group_name = "page_%s" % self.start_name
        async_to_sync(self.channel_layer.group_add)(
            self.start_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        """Disconnect group from channel layer."""
        async_to_sync(self.channel_layer.group_discard)(
            self.start_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """Receive and process messages."""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        if message.get("type") == "game_over":
            print("Hello")
            user: User = User.objects.get(id=message.get("user_id"))
            rival: User = User.objects.get(id=message.get("rival_id"))
            result: int = message.get("result")
            Result.objects.create(player=user, rival=rival.username, count=result)
        async_to_sync(self.channel_layer.group_send)(
            self.start_group_name, {"type": "play_message", "message": message}
        )

    def play_message(self, event):
        """Send message."""
        self.send(text_data=json.dumps(event))


class ProposeToPlay(WebsocketConsumer):
    """Class socket server for start page."""

    def __init__(self, *args, **kwargs) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.player_id = None
        self.propose_group_name = None

    def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.propose_group_name = "proposal_%s" % self.player_id
        async_to_sync(self.channel_layer.group_add)(
            self.propose_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        """Disconnect group from channel layer."""
        async_to_sync(self.channel_layer.group_discard)(
            self.propose_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """Receive and process messages."""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.propose_group_name, {"type": "play_message", "message": message}
        )

    def play_message(self, event):
        """Send message."""
        self.send(text_data=json.dumps(event))
