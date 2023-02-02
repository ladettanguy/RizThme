import asyncio
import logging
import discord

from random import randint
from threading import Thread, Semaphore
from typing import Tuple, Optional, Dict
from multipledispatch import dispatch

from rizthme.exception import DuplicateGuildPlayerThreadError
from rizthme.models.musics import SimpleMusic, Playlist
from rizthme.models.music_queue import MusicQueue
from rizthme.models.mode import MODE
from rizthme.models.factory import AudioFactory


class Player(Thread):
    _guild_thread: Dict[discord.Guild, "Player"] = {}

    @classmethod
    def get(cls, guild: discord.Guild) -> "Player":
        """
        Get the player of the guild
        :param guild: discord.Guild
        :return: Player
        """
        return cls._guild_thread[guild]

    @classmethod
    def setup_music_queue(cls, client: discord.Client):
        """
        Create a thread by discord.Guild where the CLIENT is present
        """
        for guild in client.guilds:
            # Starting a Player per guild
            try:
                Player(guild).start()
            except DuplicateGuildPlayerThreadError:
                pass

    @classmethod
    def set_voice_client(cls, guild: discord.Guild, voice_client: discord.VoiceClient):
        """
        Set to the appropriate thread, the voice client needed to play song
        :param guild: discord.Guild, Guild wanted to set the voice client
        :param voice_client: discord.VoiceClient
        """
        cls.get(guild)._voice_client = voice_client

    @classmethod
    def add_music(cls, message: discord.Message):
        """
        Add a music in the queue of the appropriate Guild
        :param message: discord.Message
        """
        music = AudioFactory.create_playable(message)
        guild: discord.Guild = message.guild if message.guild is not None else message.author.guild
        cls.get(guild)._add_queue(music)

    def __init__(self, guild: discord.Guild):
        super().__init__()
        self._guild: discord.Guild = guild
        if self._guild in self._guild_thread:
            logging.critical('PlayerThread created 2 time for 1 Guild')
            raise DuplicateGuildPlayerThreadError(self._guild)
        self._guild_thread[guild] = self
        self._voice_client: Optional[discord.VoiceClient] = None
        self._currently_playing_music: Optional[SimpleMusic] = None
        self._semaphore_is_playing: Semaphore = Semaphore(0)
        self._semaphore_queue: Semaphore = Semaphore(0)
        self._queue = MusicQueue(self._semaphore_queue)
        self._mode = MODE.NORMAL
        self._running = True

    def delete_thread(self):
        """
        Delete the thread
        """
        self._running = False
        self._semaphore_is_playing.release()
        self._semaphore_queue.release()
        self._guild_thread.pop(self._guild)

    def run(self):
        while self._running:
            # Wait a music in the queue
            self._semaphore_queue.acquire()
            if not self._running:  # If the player is not running, stop the thread
                break
            # Get the music to play
            index = randint(0, len(self._queue) - 1) if self._mode == MODE.SHUFFLE else 0
            self._currently_playing_music: SimpleMusic = self._queue[index]

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
            if self._queue:
                self._queue.pop(0)
        else:
            self._semaphore_queue.release()

        self._semaphore_is_playing.release()
        # Set the music currently playing to None if the queue is empty
        if not self._queue:
            asyncio.run_coroutine_threadsafe(self._guild.voice_client.disconnect(), asyncio.get_event_loop())
            self._currently_playing_music = None

    def get_now_played(self) -> Optional[Tuple[str, str]]:
        """
        Get a Tuple of the current music playing

        Metadata -> Tuple[ < Song Title >, < Song URL > ]

        :return: Tuple[str, str] or None
        """
        if self._currently_playing_music:
            return self._currently_playing_music.get_title(), self._currently_playing_music.get_url()

    @dispatch(SimpleMusic)
    def _add_queue(self, music: SimpleMusic):
        """
        Add a music in the queue of the appropriate Guild
        :param music: Music
        """
        self._queue.add_music(music)

    @dispatch(Playlist)
    def _add_queue(self, playlist: Playlist):
        """
        Add a playlist in the queue of the appropriate Guild
        :param playlist: Playlist
        """
        self._queue.add_music(playlist)

    def clear_queue(self):
        """
        Clear the music queue of the Guild
        (used for the stop command)
        """
        self._semaphore_queue = Semaphore(0)
        self._queue = MusicQueue(self._semaphore_queue)
        self._mode = MODE.NORMAL
        if self._voice_client.is_paused():
            self._voice_client.resume()
        if self._voice_client and self._voice_client.is_playing():
            self._currently_playing_music.stop(self._voice_client)
        self._currently_playing_music = None

    def set_mode(self, mode: MODE):
        """
        Set the loop mode of the music player
        :param mode: MODE
        """
        self._mode = mode
