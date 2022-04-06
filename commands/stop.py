import discord

from models import Player
from models.mode import MODE


async def stop(message: discord.Message):
    """
    Stop the music of your current Guild
    :param message: discord.Message
    """
    guild = message.guild or message.author.guild

    p = Player.get(guild)
    p.clear_queue()
    p.set_mode(MODE.NORMAL)
