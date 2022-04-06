import logging

from setting import CLIENT
from models import Player


@CLIENT.event
async def on_guild_remove(guild):
    """
    When a guild is removed, remove the music players linked to it.

    :param guild: The guild that was removed.
    :type guild: discord.Guild
    """
    logging.info(f'{guild.name} has been removed')
    Player.get(guild).delete_thread()
