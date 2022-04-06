import logging
from typing import Callable

import discord

from multipledispatch import dispatch
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from exception import BadLinkError
from .music import Music


class YTMusic(Music):
    """
    Class for handling music from YouTube.
    """

    @dispatch(str, discord.TextChannel)
    def __init__(self, url: str, channel: discord.TextChannel):
        super().__init__(url, channel)
        try:
            ytb: YouTube = YouTube(url)
        except RegexMatchError as e:
            raise BadLinkError(self._original_url) from e
        self._duration = ytb.length
        self._title: str = ytb.title
        self._stream_url: str = ytb.streams.filter(only_audio=True).order_by('abr').desc().first().url

    @dispatch(YouTube, discord.TextChannel)
    def __init__(self, youtube: YouTube, channel: discord.TextChannel):
        super().__init__(youtube.watch_url, channel)
        self._duration = youtube.length
        self._title = youtube.title
        self._stream_url = youtube.streams.filter(only_audio=True).order_by('abr').desc().first().url

    def is_valid(self, send_message: bool = False) -> bool:
        """
        Check if the Music instance is correctly playable
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the music is valid and playable
        """
        return self._is_url_valid(send_message) and self._is_valid_stream(send_message)

    def _is_url_valid(self, send_message: bool = False) -> bool:
        """
        Check the user's input url, and check if is it empty
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the original_url isn't empty
        """
        valid: bool = self._original_url != ""
        if send_message and not valid:
            logging.warning("!play: Dont valid music")
            self.send("Something's wrong, try to use !play like this: \n !play [YouTube's Link]")
        return valid

    def _is_valid_stream(self, send_message: bool = False) -> bool:
        """
        Check if the audio stream from PyTube library is correct and usable
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the stream is usable
        """
        valid: bool = self._stream_url is not None
        if send_message and not valid:
            logging.critical("!play: Dont valid music")
            self.send("Something's wrong, YouTube link is unfunctionnal")
        return valid

    def get_title(self) -> str:
        """
        :return: Title of the YouTube's video
        """
        return str(self._title)

    def get_url(self) -> str:
        """
        :return: user's input URL
        """
        return str(self._original_url)

    def get_audio_source(self) -> discord.FFmpegPCMAudio:
        """
        Create a discord.FFmpegPCMAudio from the PyTube.Stream gotten in __init__

        The @before_options is here for reconnected automaticaly the voice_client to the stream
        :return: FFmpegPCMAudio usable like AudioSource for discord.VoiceClient
        """
        before_options = " -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        try:
            return discord.FFmpegPCMAudio(self._stream_url, before_options=before_options)
        except Exception as e:
            logging.critical(f'When FFmpegPCMAudio created:\n{e}')
            self.send('Error with the YouTube API function')

    def get_duration(self) -> int:
        """
        :return: duration of the YouTube's video in seconds
        """
        return self._duration

    def message_music_added(self):
        self.send(f'Music: "{self._title}", has been added')

    def play(self, voice_client: discord.VoiceClient, after: Callable = None) -> None:
        """
        Play the music with the voice_client
        :param voice_client: discord.VoiceClient, voice_client to play the music
        :param after: Callable, Optional argument for call after the music is played
        """
        voice_client.play(self.get_audio_source(), after=after)

    def stop(self, voice_client: discord.VoiceClient) -> None:
        """
        Stop the music with the voice_client
        :param voice_client: discord.VoiceClient, voice_client to stop the music
        """
        voice_client.stop()
