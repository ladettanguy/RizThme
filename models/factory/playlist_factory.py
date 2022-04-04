from abc import ABC

import discord

from ..music import YTPlaylist


class PlaylistFactory(ABC):
    """
    Factory class for creating playlist objects.
    """

    def __init__(self):
        raise NotImplementedError("This is an abstract class")

    @classmethod
    def create_music(cls, message: discord.Message) -> 'Playlist':
        """
        Create a playlist object based on the message.
        """
        url = message.content.split(" ")[-1]
        channel = message.channel
        return cls.create_YTPlaylist(url, channel)

    @staticmethod
    def create_YTPlaylist(url: str, channel: discord.TextChannel) -> YTPlaylist:
        """
        Create a YTPlaylist object based on the message.
        """
        return YTPlaylist(url, channel)
