from abc import ABC

from . import Playable, AudioItem


class SimpleMusic(AudioItem, Playable, ABC):
    """
    Abstract class for simple music.
    """
    pass
