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
            thread = Player(guild)
            cls._guild_thread[guild] = thread
            # Starting a Player per guild
            thread.start()

    @classmethod
    async def add_music(cls, message: discord.Message):
        """
        Add a music in the queue of the appropriate Guild
        :param message: discord.Message
        """
        await cls._guild_thread[message.guild].add_queue(message)

    @classmethod
    def stop_music(cls, message):
        """
        Stop the music in the queue of the appropriate Guild
        :param message: discord.Message
        """
        cls._guild_thread[message.guild].clear_queue()

    @classmethod
    def get_now_played(cls, guild: discord.Guild) -> Optional[Tuple[str, str]]:
        return cls._guild_thread[guild]._get_now_played()

    def __init__(self, guild: discord.Guild):
        super().__init__()
        self.guild: discord.Guild = guild
        if self.guild in self._guild_thread:
            raise DuplicateGuildPlayerThreadError(self.guild)
        self.queue: List[Music] = []
        self.voice_client: Optional[discord.VoiceClient] = None
        self.now_played: Optional[Tuple[str, str]] = None
        self.semaphore_is_played: Semaphore = Semaphore(0)
        self.semaphore_queue: Semaphore = Semaphore(0)

    def run(self):
        while True:
            self.semaphore_queue.acquire()
            music: Music = self.queue.pop(0)

            # Change the music playing state
            title: str = music.get_title()
            self.now_played = (title, music.get_url())

            # Nécéssaire pour que la connection soit maintenu au dela de quelque minute
            music.play(self.voice_client, after=lambda _: self._prepare_the_next_song())

            self.semaphore_is_played.acquire()

    def _prepare_the_next_song(self):
        self.semaphore_is_played.release()
        if not self.queue:
            self.now_played = None

    def _get_now_played(self) -> Optional[Tuple[str, str]]:
        if self.now_played:
            return tuple(self.now_played)

    @classmethod
    def set_voice_client(cls, guild: discord.Guild, voice_client: discord.VoiceClient):
        cls._guild_thread[guild].voice_client = voice_client

    async def add_queue(self, message: discord.Message):
        # Récupération de la vidéo via la lib YouTube
        music = YTMusic(message)
        if not music.is_valid():
            await music.send("Something's wrong, try to use !play like this: \n !play [YouTube's Link]")
        if self.voice_client.is_playing():
            await music.send(f'Music: "{music.get_title()}", has been added')
        else:
            await music.send(f'I\'m now playing: "{music.get_title()}"')
        self.queue.append(music)
        self.semaphore_queue.release()

    def clear_queue(self):
        self.semaphore_queue = Semaphore(0)
        self.queue.clear()
        if self.voice_client:
            self.voice_client.stop()
