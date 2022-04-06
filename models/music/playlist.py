import asyncio
from abc import ABC, abstractmethod

from typing import Iterable

import discord


class Playlist(ABC):

    def __init__(self, url: str, channel: discord.TextChannel):
        self._original_url = url
        self._channel = channel

    def get_list_music(self) -> Iterable["Music"]:
        """
        Get list of music from playlist
        """
        pass

    @abstractmethod
    def get_title(self) -> str:
        """
        Get playlist title
        """
        pass

    @abstractmethod
    def get_url(self) -> str:
        """
        Get playlist url
        """
        pass

    @abstractmethod
    def is_valid(self, send_message: bool = False) -> bool:
        """
        Check if playlist is valid
        """
        pass

    def send(self, message: str):
        """
        Send message to channel
        """
        asyncio.run_coroutine_threadsafe(self._channel.send(message), asyncio.get_event_loop())
