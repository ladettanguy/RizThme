import discord
from discord import FFmpegPCMAudio
from pytube import YouTube

from models.music import Music


class YTMusic(Music):

    def __init__(self, message):
        super().__init__(message)
        ytb = YouTube(self.original_url)
        self.title = ytb.title
        self.stream = ytb.streams.filter(only_audio=True).order_by('abr').desc().first().url

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
        valid: bool = self.original_url != ""
        if send_message and not valid:
            self.send("Something's wrong, try to use !play like this: \n !play [YouTube's Link]")
        return valid

    def _is_valid_stream(self, send_message: bool = False) -> bool:
        """
        Check if the audio stream from PyTube library is correct and usable
        :param send_message: bool, Optional argument for send error message in message's channel with the error stack
        :return: True if the stream is usable
        """
        valid: bool = self.stream is not None
        if send_message and not valid:
            self.send("Something's wrong, your YouTube link is unfunctionnal")
        return valid

    def get_title(self) -> str:
        """
        :return: Title of the YouTube's video
        """
        return self.title

    def get_url(self) -> str:
        """
        :return: user's input URL
        """
        return self.original_url

    def get_audio_source(self) -> FFmpegPCMAudio:
        """
        Create a discord.FFmpegPCMAudio from the PyTube.Stream gotten in __init__

        The @before_options is here for reconnected automaticaly the voice_client to the stream
        :return: FFmpegPCMAudio usable like AudioSource for discord.VoiceClient
        """
        before_options = " -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        return discord.FFmpegPCMAudio(self.stream, before_options=before_options)
