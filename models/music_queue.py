from typing import List
from threading import Semaphore, Lock
from multipledispatch import dispatch

from .threads import PlaylistQueueAdder, MusicQueueAdder
from .musics import SimpleMusic, Playlist


class MusicQueue(List[SimpleMusic]):

    def __init__(self, semaphore: Semaphore, *args):
        super().__init__(*args)
        self._queue_semaphore = semaphore
        self._is_adding_lock = Lock()

    def set_queue_semaphore(self, sem: Semaphore):
        """
        Set a new semaphore for the queue
        :param sem: The new semaphore
        """
        self._queue_semaphore = sem

    @dispatch(SimpleMusic)
    def add_music(self, music: SimpleMusic):
        # if the message is a valid song
        if music.is_valid(send_message=True):
            MusicQueueAdder(self, music, self._queue_semaphore, self._is_adding_lock).start()

    @dispatch(Playlist)
    def add_music(self, playlist: Playlist):
        playlist.send("Loading playlist... (this may take a while)")
        PlaylistQueueAdder(self, playlist, self._queue_semaphore, self._is_adding_lock).start()
