import discord
import pytube

from typing import Iterable

from pytube.helpers import DeferredGeneratorList
from .playlist import Playlist
from pytube.exceptions import RegexMatchError
from exception import BadLinkError

from .yt_music import YTMusic


class YTPlaylist(Playlist):

    def __init__(self, url: str, channel: discord.TextChannel):
        super().__init__(url, channel)
        try:
            self.plt: pytube.Playlist = pytube.Playlist(url)
        except RegexMatchError as e:
            raise BadLinkError(self._original_url) from e
        self._title = self.plt.title

    def get_url(self) -> str:
        """
        :return: the url of the playlist
        """
        return self._original_url

    def _music_generator(self) -> str:
        for youtube in self.plt.videos:
            yield YTMusic(youtube, self._channel)

    def get_list_music(self) -> Iterable[YTMusic]:
        """
        :return: the list of music in the playlist
        """
        return DeferredGeneratorList(self._music_generator())

    def get_title(self) -> str:
        """
        :return: the title of the playlist
        """
        return self._title

    def is_valid(self, send_message: bool = False) -> bool:
        """
        :return: True if the playlist is valid, False otherwise
        """
        valid = all(music.is_valid() for music in self._music_queue)
        if not valid and send_message:
            self._channel.send("One or more music in the playlist is not valid.")
        return valid
