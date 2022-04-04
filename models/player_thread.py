import asyncio
import logging
from random import randint
from threading import Thread, Semaphore
from typing import Tuple, Optional, Dict, Union

import discord

from exception import DuplicateGuildPlayerThreadError
from .music_queue import MusicQueue
from .mode import MODE
from .factory import PlaylistFactory, MusicFactory
from setting import CLIENT


class Player(Thread):

    _guild_thread: Dict[discord.Guild, "Player"] = {}

    @classmethod
    def setup_music_queue(cls):
        """
        Create a thread by discord.Guild where the CLIENT is present
        """
        for guild in CLIENT.guilds:
            # Starting a Player per guild
            Player(guild).start()

    @classmethod
    def delete_player(cls, guild: discord.Guild):
        """
        Delete the player of the guild
        :param guild: discord.Guild
        """
        player = cls._guild_thread[guild]
        player._delete_thread()
        cls._guild_thread.pop(guild)

    @classmethod
    def set_voice_client(cls, guild: discord.Guild, voice_client: discord.VoiceClient):
        """
        Set to the appropriate thread, the voice client needed to play song
        :param guild: discord.Guild, Guild wanted to set the voice client
        :param voice_client: discord.VoiceClient
        """
        cls._guild_thread[guild]._voice_client = voice_client

    @classmethod
    def add_music(cls, message: discord.Message):
        """
        Add a music in the queue of the appropriate Guild
        :param message: discord.Message
        """
        music = MusicFactory.create_music(message)
        guild: discord.Guild = message.guild if message.guild is not None else message.author.guild
        cls._guild_thread[guild]._add_queue(music)

    @classmethod
    def add_playlist(cls, message: discord.Message):
        """
        Add a playlist in the queue of the appropriate Guild
        :param message: discord.Message
        """
        playlist = PlaylistFactory.create_music(message)
        guild: discord.Guild = message.guild if message.guild is not None else message.author.guild
        cls._guild_thread[guild]._add_queue(playlist)

    @classmethod
    def stop_music(cls, guild: discord.Guild):
        """
        Stop the music in the queue of the appropriate Guild
        :param guild: discord.Guild
        """
        cls._guild_thread[guild]._clear_queue()

    @classmethod
    def get_now_played(cls, guild: discord.Guild) -> Optional[Tuple[str, str]]:
        """
        Get a Tuple of the current music playing

        Metadata -> Tuple[ < Song Title >, < Song URL > ]

        :param guild: discord.Guild, guild of the music player wanted
        :return: Tuple[str, str] or None
        """
        return cls._guild_thread[guild]._get_now_played()

    @classmethod
    def set_mode(cls, guild: discord.Guild, mode: MODE):
        """
        Set the loop mode of the music player
        :param guild: discord.Guild
        :param mode: int, mode wanted
        """
        cls._guild_thread[guild]._set_mode(mode)

    def __init__(self, guild: discord.Guild):
        super().__init__()
        self._guild: discord.Guild = guild
        if self._guild in self._guild_thread:
            logging.critical('PlayerThread created 2 time for 1 Guild')
            raise DuplicateGuildPlayerThreadError(self._guild)
        self._guild_thread[guild] = self
        self._queue = MusicQueue()
        self._voice_client: Optional[discord.VoiceClient] = None
        self._currently_playing_music: Optional["Music"] = None
        self._semaphore_is_playing: Semaphore = Semaphore(0)
        self._semaphore_queue: Semaphore = Semaphore(0)
        self._mode = MODE.NORMAL
        self._running = True

    def run(self):
        while self._running:
            # Wait a music in the queue
            self._semaphore_queue.acquire()
            if not self._running:  # If the player is not running, stop the thread
                break

            # Get the music to play
            index = randint(0, len(self._queue)-1) if self._mode == MODE.SHUFFLE else 0
            self._currently_playing_music: "Music" = self._queue[index]

            # Play the music
            self._currently_playing_music.play(self._voice_client, after=lambda _: self._prepare_the_next_song())

            # Wait the music.play callback for continue
            self._semaphore_is_playing.acquire()

    def _prepare_the_next_song(self):
        """
        This private method is here to release the @semaphore_is_playing
        and used for the callback function after a song playing.
        """
        if self._mode == MODE.NORMAL:
            self._queue.pop(0)
        self._semaphore_is_playing.release()
        # Set the music currently playing to None if the queue is empty
        if not self._queue:
            asyncio.run_coroutine_threadsafe(self._guild.voice_client.disconnect(), CLIENT.loop)
            self._currently_playing_music = None

    def _get_now_played(self) -> Optional[Tuple[str, str]]:
        """
        Get a Tuple of the current music playing

        Metadata -> Tuple[ < Song Title >, < Song URL > ]

        :return: Tuple[str, str] or None
        """
        if self._currently_playing_music:
            return self._currently_playing_music.get_title(),  self._currently_playing_music.get_url()

    def _add_queue(self, playable: Union["Music", "Playlist"]):
        """
        Add a music in the queue of the appropriate Guild
        :param playable: Music or Playlist
        """

        self._queue.add_music(playable)
        self._semaphore_queue.release()

    def _clear_queue(self):
        """
        Clear the music queue of the Guild
        (used for the stop command)
        """
        self._semaphore_queue = Semaphore(0)
        self._queue.clear()
        if self._voice_client:
            self._currently_playing_music.stop(self._voice_client)

    def _set_mode(self, mode: MODE):
        """
        Set the loop mode of the music player
        :param mode: MODE
        """
        self._mode = mode

    def _delete_thread(self):
        """
        Delete the music player thread

        To do this, we set the @_running to False, and release all semaphores for continue into the @run end.
        And when @run is finished, the player thread will be deleted.
        """
        self._running = False
        self._semaphore_is_playing.release()
        self._semaphore_queue.release()
