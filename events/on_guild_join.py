import logging
import discord

from models.threads import Player


async def on_guild_join(client: discord.Client, guild: discord.Guild):
    """
    this event is called when a new guild is joined or created by the CLIENT.
    
    :param client: Client discord
    :param guild: The guild that was joined.
    """
    logging.info(f"Joined guild {guild.name}")
    Player(guild).start()
