from typing import List
from threading import Semaphore
from multipledispatch import dispatch

from .playlist_queue_adder import PlaylistQueueAdder

from .music import Music, Playlist


class MusicQueue(List[Music]):

    def __init__(self, semaphore: Semaphore, *args):
        super().__init__(*args)
        self._semaphore = semaphore

    def set_semaphore(self, sem: Semaphore):
        """
        Set a new semaphore for the queue
        :param sem: The new semaphore
        """
        self._semaphore = sem

    @dispatch(Music)
    def add_music(self, music: Music):
        # if the message is not a valid song
        if not music.is_valid(send_message=True):
            pass
        music.send(f'Music: "{music.get_title()}", has been added')
        # Add music to the queue, and release the @_semaphore_queue
        self.append(music)
        self._semaphore.release()

    @dispatch(Playlist)
    def add_music(self, playlist: Playlist):
        PlaylistQueueAdder(self, self._semaphore, playlist).start()
