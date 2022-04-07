from threading import Thread, Semaphore, Lock
from typing import List

from models.musics import Playlist, SimpleMusic


class PlaylistQueueAdder(Thread):
    """
    Thread to add all music from a playlist to the queue, without blocking the main thread progress.
    """

    def __init__(self, queue: List[SimpleMusic], playlist: Playlist,
                 queue_semaphore: Semaphore, _is_adding_lock: Lock):
        super().__init__()
        self._queue = queue
        self._queue_semaphore = queue_semaphore
        self._is_adding_lock = _is_adding_lock
        self._playlist = playlist

    def run(self):
        self._is_adding_lock.acquire()
        for music in self._playlist.get_list_music():
            if music.is_valid(send_message=True):
                self._queue.append(music)
                self._queue_semaphore.release()
        self._playlist.send(f"Playlist: {self._playlist.get_title()} has been added")
        self._is_adding_lock.release()
