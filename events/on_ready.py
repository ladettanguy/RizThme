import logging

from setting import CLIENT
from models import Player


@CLIENT.event
async def on_ready():
    """
    On_ready event run after the client connection is established and the login is successful.

    It's used to set up differents settings and variables.
    """
    # Setup Players Guild's thread
    Player.setup_music_queue()
    logging.info('Client Ready')
