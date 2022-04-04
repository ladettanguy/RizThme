import discord
import pytube

from typing import List

from .playlist import Playlist
from pytube.exceptions import RegexMatchError
from exception import BadLinkError

from .yt_music import YTMusic


class YTPlaylist(Playlist):

    def __init__(self, url: str, channel: discord.TextChannel):
        super().__init__(url, channel)
        try:
            plt: pytube.Playlist = pytube.Playlist(url)
        except RegexMatchError as e:
            raise BadLinkError(self._original_url) from e
        url_list = plt.video_urls
        self._title = plt.title
        self._music_queue = [YTMusic(url, channel) for url in url_list]

    def get_url(self) -> str:
        """
        :return: the url of the playlist
        """
        return self._original_url

    def get_list_music(self) -> List[YTMusic]:
        """
        :return: the list of music in the playlist
        """
        return self._music_queue

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
