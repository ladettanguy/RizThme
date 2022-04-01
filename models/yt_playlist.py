from random import Random
from typing import Callable, Optional

import discord
from pytube import Playlist
from pytube.exceptions import RegexMatchError

from exception import BadLinkError
from models import Music, YTMusic


class YTPlaylist(Music):

    def __init__(self, message: discord.Message):
        super().__init__(message)
        try:
            plt: Playlist = Playlist(self._original_url)
        except RegexMatchError as e:
            raise BadLinkError(self._original_url) from e
        url_list = plt.video_urls
        self._currently_index_playing = 0
        self._music_queue = [YTMusic(url) for url in url_list]
        self._loop: bool = False
        self._shuffle: bool = False

    def is_valid(self, send_message: bool = False) -> bool:
        return all(music.is_valid(send_message) for music in self._music_queue)

    def get_audio_source(self) -> discord.AudioSource:
        """
        :return: discord.AudioSource, the currently playing audio source
        """
        return self._music_queue[self._currently_index_playing].get_audio_source()

    def get_title(self) -> str:
        """
        :return: str, title of the currently playing song
        """
        return f'{self._music_queue[self._currently_index_playing].get_title()}'

    def get_duration(self) -> int:
        """
        :return: int, duration of the currently playing song
        """
        return self._music_queue[self._currently_index_playing].get_duration()

    def get_url(self) -> str:
        """
        :return: str, YouTube url of the currently playing song
        """
        return self._music_queue[self._currently_index_playing].get_url()

    def play(self, voice_client: discord.VoiceClient, after: Callable = None):
        """
        Play the playlist in the voice_client and execute the callback function @after when it's finish
        :param voice_client: discord.VoiceClient, voice client to play the music
        :param after: Callable, function to call after the music is finished playing
        """
        song = self._music_queue[self._currently_index_playing]
        song.play(voice_client, after=lambda _: self._callback_timer(voice_client, after))

    def _callback_timer(self, voice_client: discord.VoiceClient, after) -> Optional[Callable]:
        """
        Callback function to be executed after the music is finished playing

        here, we use a retarded callback because we need to wait for the voice_client to be ready

        :param voice_client: discord.VoiceClient, voice client to play the music
        :param after: Callable, function to call after the music is finished playing
        :return: Callable, function to call after the music is finished playing
        """
        if self._shuffle:
            rand = Random.randint(0, len(self._music_queue)-1)
            self._currently_index_playing = rand if rand != self._currently_index_playing else rand - 1
        self._currently_index_playing += 1
        if self._currently_index_playing >= len(self._music_queue):
            if self._loop:
                self._currently_index_playing = 0
                self._music_queue[self._currently_index_playing].play(voice_client, after)
            else:
                return after
