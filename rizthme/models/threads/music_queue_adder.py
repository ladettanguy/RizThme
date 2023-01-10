from threading import Thread, Semaphore, Lock
from typing import List

from rizthme.models.musics import SimpleMusic


class MusicQueueAdder(Thread):
    """
    Thread to add all music from a playlist to the queue, without blocking the main thread progress.
    """

    def __init__(self, queue: List[SimpleMusic], music: SimpleMusic,
                 queue_semaphore: Semaphore, _is_adding_lock: Lock):
        super().__init__()
        self._queue = queue
        self._queue_semaphore = queue_semaphore
        self._is_adding_lock = _is_adding_lock
        self._music = music

    def run(self):
        self._is_adding_lock.acquire()
        self._queue.append(self._music)
        self._queue_semaphore.release()
        self._music.send(f'Music: "{self._music.get_title()}", has been added')
        self._is_adding_lock.release()
