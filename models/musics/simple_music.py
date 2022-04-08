from abc import ABC

from .audio_item import AudioItem
from .playable import Playable


class SimpleMusic(AudioItem, Playable, ABC):
    """
    Abstract class for music.
    """
    pass
