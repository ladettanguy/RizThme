from threading import Thread, Semaphore
from typing import List

from models.music import Playlist, Music


class PlaylistQueueAdder(Thread):
    """
    Thread to add all music from a playlist to the queue, without blocking the main thread progress.
    """

    def __init__(self, queue: List[Music], semaphore: Semaphore, playlist: Playlist):
        super().__init__()
        self._queue = queue
        self._semaphore = semaphore
        self._playlist = playlist

    def run(self):
        for music in self._playlist.get_list_music():
            if music.is_valid(send_message=True):
                self._queue.append(music)
                self._semaphore.release()
        self._playlist.send(f"Playlist: {self._playlist.get_title()} has been added")
