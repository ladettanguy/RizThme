import discord

from models import Player
from models.mode import MODE


async def loop(message: discord.Message):
    """
    Setting up the loop mode to the music player in the guild.
    """
    guild: discord.Guild = message.guild or message.author.guild
    Player.get(guild).set_mode(MODE.LOOP)
    await message.channel.send('Mode: Loop activeted !')
