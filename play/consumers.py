"""Consumers for 'play' app."""
import json
from typing import Any, Dict, Optional

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.cache import cache

from config.settings import CACHE_TTL
from play.constants import (
    initial_board,
    play_consumers_message_types_set,
    start_consumers_message_types_set,
)
from play.models import ResultData
from play.play_helpers import get_all_users_data


class BasePlayConsumer(AsyncWebsocketConsumer):
    """Class socket server for playing page."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.play_group_name: Optional[str] = None
        self.player_id: Optional[int] = None
        self.rival_id: Optional[int] = None
        self.user: Optional[User] = None

    async def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.player_id = self.scope['url_route']['kwargs']['player_id']
        self.rival_id = self.scope['url_route']['kwargs']['rival_id']
        self.play_group_name = 'play_{player}_{rival}'.format(
            player=self.player_id,
            rival=self.rival_id,
        )
        self.user = self.scope.get('user')
        if self.user and self.user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(self.play_group_name, self.channel_name)
            board_info = cache.get(self.play_group_name, {})
            if not board_info:
                board_info = {
                    'board': initial_board,
                    'player': 1,
                }
            await self.channel_layer.group_send(
                self.play_group_name,
                {
                    'type': 'user_play_join_message',
                    'message': {
                        'user_id': self.user.pk,
                        'board': board_info.get('board'),
                        'player': board_info.get('player'),
                    },
                },
            )

    async def disconnect(self, code: int) -> None:
        """Disconnect group from channel layer."""
        await self.channel_layer.group_discard(self.play_group_name, self.channel_name)
        if self.user and self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.play_group_name,
                {
                    'type': 'user_play_leave_message',
                    'message': {'user_id': self.user.pk},
                },
            )

    async def receive(
        self,
        text_data: Optional[bytes] = None,
        bytes_data: Optional[bytes] = None,
    ) -> None:
        """Receive and process messages."""
        if self.user and self.user.is_authenticated and text_data:
            text_data_json: Dict = json.loads(text_data)
            message_type: str = text_data_json.get('type', '')
            if message_type not in play_consumers_message_types_set:
                return
            message: dict = text_data_json.get('message', {})
            if message_type == 'play_message':
                cache.set(
                    self.play_group_name,
                    {
                        'board': message.get('board', ''),
                        'player': message.get('player', ''),
                    },
                    CACHE_TTL,
                )
            if message_type == 'user_message':
                message['username'] = self.user.username
            await self.channel_layer.group_send(
                self.play_group_name,
                {'type': message_type, 'message': message},
            )

    async def play_message(self, event: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event))

    async def user_message(self, event: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event))

    async def ask_rival(self, event: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event))


class PlayConsumer(BasePlayConsumer):
    """Class with PlayConsumer methods."""

    async def answer_rival(self, event_val: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_val))

    async def user_play_join_message(self, event_val: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_val))

    async def user_play_leave_message(self, event_val: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_val))

    async def propose_draw(self, event_val: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_val))

    async def agree_draw(self, event_val: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_val))

    async def refuse_draw(self, event_val: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_val))


class BaseStartConsumer(AsyncWebsocketConsumer):
    """Class socket server for start page."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Add custom class attributes."""
        super().__init__(*args, **kwargs)
        self.start_name: Optional[int] = None
        self.start_group_name: Optional[str] = None
        self.user: Optional[User] = None

    async def connect(self) -> None:
        """Add/connect group to channel layer."""
        self.start_name = self.scope['url_route']['kwargs']['player_id']
        self.start_group_name = 'page_{string}'.format(string=self.start_name)
        self.user = self.scope.get('user')
        await self.accept()
        await self.channel_layer.group_add(self.start_group_name, self.channel_name)
        if self.user and self.user.is_authenticated:
            profile_data = await get_all_users_data().aget(id=self.user.pk)
            user_data = {
                'plays': profile_data.plays_number,
                'loses': profile_data.loses,
                'draws': profile_data.draws,
                'wins': profile_data.wins,
                'points': profile_data.points,
            }
            await self.channel_layer.group_send(
                self.start_group_name,
                {
                    'type': 'user_join_message',
                    'message': {
                        'user_id': self.user.pk,
                        'username': self.user.username,
                        'user_data': user_data,
                    },
                },
            )

    async def disconnect(self, code: int) -> None:
        """Disconnect group from channel layer."""
        await self.channel_layer.group_discard(self.start_group_name, self.channel_name)
        if self.user and self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.start_group_name,
                {
                    'type': 'user_leave_message',
                    'message': {
                        'user_id': self.user.pk,
                        'username': self.user.username,
                    },
                },
            )

    async def receive(
        self,
        text_data: Optional[bytes] = None,
        bytes_data: Optional[bytes] = None,
    ) -> None:
        """Receive and process messages."""
        if self.user and self.user.is_authenticated and text_data:
            text_data_json: Dict = json.loads(text_data)
            message_type: str = text_data_json.get('type', '')
            if message_type not in start_consumers_message_types_set:
                return
            message: Dict = text_data_json.get('message', {})
            if message_type == 'game_over':
                user_id = message.get('user_id')
                rival_id = message.get('rival_id')
                if message.get('white'):
                    cache.delete(
                        'play_{user_id}_{rival_id}'.format(
                            user_id=user_id,
                            rival_id=rival_id,
                        ),
                    )
                else:
                    cache.delete(
                        'play_{rival_id}_{user_id}'.format(
                            rival_id=rival_id,
                            user_id=user_id,
                        ),
                    )
                await ResultData.objects.acreate(
                    player_id=user_id,
                    rival_id=rival_id,
                    count=message.get('result'),
                )
            elif message_type == 'user_message':
                message['username'] = self.user.username
            await self.channel_layer.group_send(
                self.start_group_name,
                {'type': message_type, 'message': message},
            )

    async def game_over(self, event: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event))

    async def start_playing(self, event: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event))


class StartConsumer(BaseStartConsumer):
    """Class with StartConsumer methods."""

    async def refresh(self, event_value: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_value))

    async def user_message(self, event_value: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_value))

    async def user_join_message(self, event_value: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_value))

    async def user_leave_message(self, event_value: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_value))

    async def propose(self, event_value: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_value))

    async def agree(self, event_value: bytes) -> None:
        """Send message."""
        await self.send(text_data=json.dumps(event_value))
