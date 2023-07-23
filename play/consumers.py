"""Consumers for 'play' app."""
import json
from typing import Any, Dict, Optional, Union

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from play.models import Result
from play.utils import get_all_users_data


class PlayConsumer(WebsocketConsumer):
    """Class socket server for playing page."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.play_group_name: Optional[str] = None
        self.player_id: Optional[int] = None
        self.rival_id: Optional[int] = None
        self.user: Optional[User] = None

    def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.rival_id = self.scope["url_route"]["kwargs"]["rival_id"]
        self.play_group_name = f"play_{self.player_id}_{self.rival_id}"
        self.user = self.scope.get("user")
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.play_group_name, self.channel_name
        )

    def disconnect(self, code: int) -> None:
        """Disconnect group from channel layer."""
        async_to_sync(self.channel_layer.group_discard)(
            self.play_group_name, self.channel_name
        )

    def receive(
        self, text_data: Optional[bytes] = None, bytes_data: Optional[bytes] = None
    ) -> None:
        """Receive and process messages."""
        if text_data:
            text_data_json: Dict = json.loads(text_data)
            message: Union[str, Dict] = text_data_json["message"]
            if not self.user.is_authenticated:
                return
            async_to_sync(self.channel_layer.group_send)(
                self.play_group_name, {"type": "play_message", "message": message}
            )

    def play_message(self, event: bytes) -> None:
        """Send message."""
        self.send(text_data=json.dumps(event))


class StartConsumer(WebsocketConsumer):
    """Class socket server for start page."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.start_name: Optional[int] = None
        self.start_group_name: Optional[str] = None
        self.user: Optional[User] = None

    def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.start_name = self.scope["url_route"]["kwargs"]["player_id"]
        self.start_group_name = "page_%s" % self.start_name
        self.user = self.scope.get("user")
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.start_group_name, self.channel_name
        )
        if self.user.is_authenticated:
            profile_data = get_all_users_data().get(id=self.user.pk)
            user_data = {
                "plays": profile_data.plays_number,
                "loses": profile_data.loses,
                "draws": profile_data.draws,
                "wins": profile_data.wins,
                "points": profile_data.points,
            }
            async_to_sync(self.channel_layer.group_send)(
                self.start_group_name,
                {
                    "type": "user_join_message",
                    "message": {
                        "user_id": self.user.pk,
                        "username": self.user.username,
                        "user_data": user_data,
                    },
                }
            )

    def disconnect(self, code: int) -> None:
        """Disconnect group from channel layer."""
        async_to_sync(self.channel_layer.group_discard)(
            self.start_group_name, self.channel_name
        )
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.start_group_name,
                {
                    "type": "user_leave_message",
                    "message": {
                        "user_id": self.user.pk,
                        "username": self.user.username,
                    }
                }
            )

    def receive(
        self, text_data: Optional[bytes] = None, bytes_data: Optional[bytes] = None
    ) -> None:
        """Receive and process messages."""
        if text_data:
            text_data_json: Dict = json.loads(text_data)
            message: Dict = text_data_json["message"]
            if not self.user.is_authenticated:
                return
            if message.get("type") == "game_over":
                user: User = User.objects.get(id=message.get("user_id"))
                rival: User = User.objects.get(id=message.get("rival_id"))
                result: Optional[int] = message.get("result")
                Result.objects.create(player=user, rival=rival.username, count=result)
            # if message.get("type") == "user_data":
            #     async_to_sync(self.channel_layer.group_send)(
            #         self.start_group_name, {"type": "user_message", "message": message}
            #     )
            # else:
            async_to_sync(self.channel_layer.group_send)(
                self.start_group_name, {"type": "start_message", "message": message}
            )

    def start_message(self, event: bytes) -> None:
        """Send message."""
        self.send(text_data=json.dumps(event))

    def user_message(self, event: bytes) -> None:
        """Send message."""
        self.send(text_data=json.dumps(event))

    def user_join_message(self, event: bytes) -> None:
        """Send message."""
        self.send(text_data=json.dumps(event))

    def user_leave_message(self, event: bytes) -> None:
        """Send message."""
        self.send(text_data=json.dumps(event))


class ProposeToPlay(WebsocketConsumer):
    """Class socket server for start page."""

    def __init__(self, *args, **kwargs) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.player_id: Optional[int] = None
        self.propose_group_name: Optional[str] = None
        self.user: Optional[User] = None

    def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]
        self.propose_group_name = "proposal_%s" % self.player_id
        self.user = self.scope.get("user")
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.propose_group_name, self.channel_name
        )

    def disconnect(self, code: int) -> None:
        """Disconnect group from channel layer."""
        async_to_sync(self.channel_layer.group_discard)(
            self.propose_group_name, self.channel_name
        )

    def receive(
        self, text_data: Optional[bytes] = None, bytes_data: Optional[bytes] = None
    ) -> None:
        """Receive and process messages."""
        if text_data:
            text_data_json: Dict = json.loads(text_data)
            message: Union[str, Dict] = text_data_json["message"]
            if not self.user.is_authenticated:
                return
            async_to_sync(self.channel_layer.group_send)(
                self.propose_group_name, {"type": "propose_message", "message": message}
            )

    def propose_message(self, event: bytes) -> None:
        """Send message."""
        self.send(text_data=json.dumps(event))
