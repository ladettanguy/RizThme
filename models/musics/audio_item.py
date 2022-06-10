import asyncio
from abc import ABC, abstractmethod

import discord

from ...setting import CLIENT


class AudioItem(ABC):

    def __init__(self, url, channel: discord.TextChannel):
        self._url = url
        self._channel = channel

    @abstractmethod
    def get_title(self) -> str:
        """
        Get title
        """
        pass

    @abstractmethod
    def get_url(self) -> str:
        """
        Get url
        """
        pass

    def send(self, message: str):
        """
        Send message to channel
        """
        asyncio.run_coroutine_threadsafe(self._channel.send(message), CLIENT.loop)
