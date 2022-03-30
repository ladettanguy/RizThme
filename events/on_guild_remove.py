import logging

from setting import CLIENT
from models import Player


@CLIENT.event
async def on_guild_remove(self, guild):
    logging.info(f'{guild.name} has been removed')
    Player.delete_player(guild)
