import logging
import discord

from models.threads import Player


async def on_ready(client: discord.Client):
    """
    this event run after the client is ready, the token is valid.

    warning: this event is not lit "on_connect".
    It's used to set up differents settings and variables.
    """
    # Setup Players Guild's thread
    Player.setup_music_queue(client)
    logging.info('Client Ready')
