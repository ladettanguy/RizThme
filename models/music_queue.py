import discord
from multipledispatch import dispatch
from typing import List

from .music import Music, Playlist


class MusicQueue(List[Music]):

    def __init__(self, *args):
        super().__init__(*args)

    @dispatch(Music)
    def add_music(self, music: Music):
        # if the message is not a valid song
        if not music.is_valid(send_message=True):
            pass
        music.send(f'Music: "{music.get_title()}", has been added')
        # Add music to the queue, and release the @_semaphore_queue
        self.append(music)

    @dispatch(Playlist)
    def add_music(self, playlist: Playlist):
        playlist.send(f"Playlist: {playlist.get_title()} has been added")
        if not playlist.is_valid(send_message=True):
            pass
        self.extend(playlist.get_list_music())
