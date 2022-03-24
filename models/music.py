from abc import ABC, abstractmethod
from typing import Optional, Callable

import discord


class Music(ABC):

    def __init__(self, message: discord.Message):
        self._message: discord.Message = message
        list_arg = message.content.split(' ')
        self._original_url = ""
        if len(list_arg) > 1:
            self._original_url = list_arg[-1]

    @abstractmethod
    def is_valid(self, send_message: bool = False) -> bool:
        """
        Check if the Music instance is correctly playable
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the music is valid and playable
        """
        pass

    @abstractmethod
    def get_audio_source(self) -> discord.AudioSource:
        """
        Create a discord.AudioSource from the init music link
        :return: discord.AudioSource usable like AudioSource for discord.VoiceClient
        """
        pass

    @abstractmethod
    def get_title(self) -> str:
        """
        :return: Title of the YouTube's video
        """
        pass

    @abstractmethod
    def get_url(self) -> str:
        """
        :return: user's input URL
        """
        pass

    def play(self, voice_client: discord.VoiceClient, after: Optional[Callable] = None):
        """
        Play the sound in the voice_client and execute the callback function @after when it's finish
        :param voice_client: discord.VoiceClient
        :param after: Optional[Callable]
        """
        voice_client.play(self.get_audio_source(), after=after)

    async def send(self, message: str):
        """
        Send a message by the discord.py API
        :param message: AnyStr, to send in the orignal message's channel
        """
        await self._message.channel.send(message)
