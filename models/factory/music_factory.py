import re
import discord

from abc import ABC

from exception import BadLinkError
from ..musics import YTMusic, YTPlaylist


class MusicFactory(ABC):
    """
    Factory class for creating music objects.
    """

    dict_regex = {
        YTMusic: r"^https?:\/\/(www.)?(youtube.com|youtube.com|youtu.be)\/watch?(.*)$",
        YTPlaylist: r"^https?:\/\/(www.)?(youtube.com|youtube.com|youtu.be)\/playlist?(.*)$",
    }

    def __init__(self):
        raise NotImplementedError("This is an abstract class")

    @classmethod
    def create_music(cls, message: discord.Message) -> "Music":
        """
        Create a music object based on the message.

        That will check by a regex if the message is a valid link.

        the @dict_regex while be used to have the regex for a specific type of music.
        """
        url = message.content.split(" ")[-1]
        channel = message.channel
        for MusicClass, regex in cls.dict_regex.items():
            if re.match(regex, url):
                return MusicClass(url, channel)
        raise BadLinkError(f'your URL "{url}" is not a valid link.')
