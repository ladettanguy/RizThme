from threading import Thread, Semaphore
from typing import List, Tuple, Optional, Dict, Union

import discord
from pytube import YouTube

from setting import CLIENT


class Player(Thread):

    def __init__(self, guild: discord.Guild):
        super().__init__()
        self.guild: discord.Guild = guild
        self.queue: List[str] = voice_queue[guild]['queue']
        self.voice_client: Optional[discord.VoiceClient] = None
        self.semaphore_is_played = Semaphore(0)

    def run(self):
        while True:
            while self.queue:
                if not self.voice_client:
                    # Récupère le VoiceClient du bot, s'il y en a déjà un présent
                    # dans le serveur au cas où il serait bug
                    self.voice_client = discord.utils.get(CLIENT.voice_clients, guild=self.guild)
                url = self.queue.pop(0)

                # Récupération de la vidéo via la lib YouTube
                ytb: YouTube = YouTube(url)

                # Change the music playing state
                title = ytb.title
                set_now_played(self.guild, (title, url))
                # Recover the audio only information
                audio = ytb.streams.filter(only_audio=True, mime_type='audio/webm').first().url
                if audio is None:
                    print("Je n'arrive pas a lire cette vidéo")
                print(audio)
                self.voice_client.play(audio, after=lambda _: self._prepare_the_next_song())
                print(f"i'm now playing: {title}")
                self.semaphore_is_played.acquire()

    def _prepare_the_next_song(self):
        self.semaphore_is_played.release()
        if not self.queue:
            print('Queue finish.')
            set_now_played(self.guild, None)

    def set_voice_client(self, voice_client: discord.VoiceClient):
        self.voice_client = voice_client


voice_queue: Dict[discord.Guild, Dict[str, Union[List[str], Player]]] = {}
now_played: Dict[discord.Guild, Optional[Tuple[str, str]]] = {}  # Dict de key=Guild, value=Tuple (nom vidéo, url)


def set_now_played(guild: discord.Guild, tuple_info: Optional[Tuple]):
    now_played[guild] = tuple_info


def get_now_played(guild: discord.Guild) -> Optional[Tuple[str, str]]:
    return now_played[guild]


def setup_music_queue():
    for guild in CLIENT.guilds:
        now_played[guild] = None
        voice_queue[guild] = {'queue': []}
        thread = Player(guild)
        voice_queue[guild]['thread'] = thread
        # Lancement d'un thread par guild
        thread.start()
