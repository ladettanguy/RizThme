import discord

from models import Player
from models.mode import MODE
from setting import CLIENT


async def loop(message: discord.Message):
    """
    Setting up the loop mode to the music player in the guild.
    """
    guild: discord.Guild = message.guild or message.author.guild

    Player.get(guild).set_mode(MODE.LOOP)
    await message.channel.send('Mode: Loop activeted !')

CLIENT.add_command(["loop"], loop)
