import logging

from setting import CLIENT
from models import Player


@CLIENT.event
async def on_ready():
    """
    this event run after the client is ready, the token is valid.

    warning: this event is not lit "on_connect".
    It's used to set up differents settings and variables.
    """
    # Setup Players Guild's thread
    Player.setup_music_queue()
    logging.info('Client Ready')
