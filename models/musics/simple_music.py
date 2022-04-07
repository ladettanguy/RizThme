from abc import ABC, abstractmethod
from typing import Optional, Callable

import discord

from .audio_item import AudioItem


class SimpleMusic(AudioItem, ABC):
    """
    Abstract class for music.
    """

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
    def get_duration(self) -> int:
        """
        :return: duration of the music in seconds
        """
        pass

    @abstractmethod
    def play(self, voice_client: discord.VoiceClient, after: Optional[Callable] = None):
        """
        Play the sound in the voice_client and execute the callback function @after when it's finish
        :param voice_client: discord.VoiceClient
        :param after: Optional[Callable]
        """
        pass

    @abstractmethod
    def stop(self, voice_client: discord.VoiceClient):
        """
        Stop the music in the voice_client
        :param voice_client: discord.VoiceClient
        """
        pass
