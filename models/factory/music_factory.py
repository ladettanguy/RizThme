from abc import ABC

import discord

from ..music import YTMusic


class MusicFactory(ABC):
    """
    Factory class for creating music objects.
    """

    def __init__(self):
        raise NotImplementedError("This is an abstract class")

    @classmethod
    def create_music(cls, message: discord.Message) -> "Music":
        """
        Create a music object based on the message.
        """
        url = message.content.split(" ")[-1]
        channel = message.channel
        return cls.create_YTMusic(url, channel)

    @staticmethod
    def create_YTMusic(url: str, channel: discord.TextChannel) -> YTMusic:
        """
        Creates a YTMusic object based on the message.
        """
        return YTMusic(url, channel)
