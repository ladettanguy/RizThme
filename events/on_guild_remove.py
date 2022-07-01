import logging
import discord
from models.threads import Player


async def on_guild_remove(client: discord.Client, guild: discord.Guild):
    """
    When a guild is removed, remove the music players linked to it.

    :param client: Client discord
    :param guild: The guild that was removed.
    :type guild: discord.Guild
    """
    logging.info(f'{guild.name} has been removed')
    Player.get(guild).delete_thread()
