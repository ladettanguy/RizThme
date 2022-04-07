import discord
import pytube


from typing import Iterable

from pytube.helpers import DeferredGeneratorList
from ..playlist import Playlist

from .yt_music import YTMusic


class YTPlaylist(Playlist):

    def __init__(self, url: str, channel: discord.TextChannel):
        super().__init__(url, channel)
        self.plt: pytube.Playlist = pytube.Playlist(url)
        self._title = self.plt.title

    def get_url(self) -> str:
        """
        :return: the url of the playlist
        """
        return self._url

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
