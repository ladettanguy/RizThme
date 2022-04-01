import asyncio
import logging
from threading import Thread, Semaphore
from typing import List, Tuple, Optional, Dict

import discord

from exception import DuplicateGuildPlayerThreadError
from models import Music, YTMusic
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
        player.delete_thread()
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
    async def add_music(cls, message: discord.Message):
        """
        Add a music in the queue of the appropriate Guild
        :param message: discord.Message
        """
        await cls._guild_thread[message.guild]._add_queue(message)

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

    def __init__(self, guild: discord.Guild):
        super().__init__()
        self._guild: discord.Guild = guild
        if self._guild in self._guild_thread:
            logging.critical('PlayerThread created 2 time for 1 Guild')
            raise DuplicateGuildPlayerThreadError(self._guild)
        self._guild_thread[guild] = self
        self._queue: List[Music] = []
        self._voice_client: Optional[discord.VoiceClient] = None
        self._now_played: Optional[Tuple[str, str]] = None
        self._currently_playing_music: Optional[YTMusic] = None
        self._semaphore_is_playing: Semaphore = Semaphore(0)
        self._semaphore_queue: Semaphore = Semaphore(0)
        self._running = True

    def run(self):
        while self._running:
            # Wait a music in the queue
            self._semaphore_queue.acquire()
            if not self._running:  # If the player is not running, stop the thread
                break
            music: Music = self._queue.pop(0)

            # Change the music currently playing
            title: str = music.get_title()
            url: str = music.get_url()
            self._now_played = (title, url)

            music.play(self._voice_client, after=lambda _: self._prepare_the_next_song())

            # Wait the music.play callback for continue
            self._semaphore_is_playing.acquire()

    def _prepare_the_next_song(self):
        """
        This private method is here to release the @semaphore_is_playing
        and used for the callback function after a song playing.
        """
        self._semaphore_is_playing.release()
        # Set the music currently playing to None if the queue is empty
        if not self._queue:
            asyncio.run_coroutine_threadsafe(self._guild.voice_client.disconnect(), CLIENT.loop)
            self._now_played = None

    def _get_now_played(self) -> Optional[Tuple[str, str]]:
        """
        Get a Tuple of the current music playing

        Metadata -> Tuple[ < Song Title >, < Song URL > ]

        :return: Tuple[str, str] or None
        """
        if self._now_played:
            return tuple(self._now_played)

    async def _add_queue(self, message: discord.Message):
        """
        Add a music in the queue of the appropriate Guild
        :param message: discord.Message
        """
        # Create the Music instance for this message
        music: Music = YTMusic(message)
        # if the message is not a valid song
        if not music.is_valid(send_message=True):
            pass
        elif self._voice_client.is_playing():
            await music.send(f'Music: "{music.get_title()}", has been added')
        else:
            await music.send(f'I\'m now playing: "{music.get_title()}"')
        # Add music to the queue, and release the @_semaphore_queue
        self._queue.append(music)
        self._semaphore_queue.release()

    def stop_music(self):
        """
        Stop the music in the queue of the appropriate Guild
        """
        self._running = False
        if self._queue:
            self._queue.clear()
            self._semaphore_queue.release()
            self._currently_playing_music.stop(self._voice_client)

    def _clear_queue(self):
        """
        Clear the music queue of the Guild
        (used for the stop command)
        """
        self._semaphore_queue = Semaphore(0)
        self._queue.clear()
        if self._voice_client:
            self._voice_client.stop()

    def delete_thread(self):
        """
        Delete the music player thread

        To do this, we set the @_running to False, and release all semaphores for continue into the @run end.
        And when @run is finished, the player thread will be deleted.
        """
        self._running = False
        self._semaphore_is_playing.release()
        self._semaphore_queue.release()
