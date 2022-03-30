import logging
import discord

from models import Player
from setting import CLIENT


@CLIENT.event
async def on_guild_join(guild: discord.Guild):
    """
    this event is called when a new guild is joined or created by the CLIENT.
    
    :param guild: The guild that was joined.
    """
    logging.info(f"Joined guild {guild.name}")
    Player(guild).start()
