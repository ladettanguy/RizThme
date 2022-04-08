import discord

from models import Player
from models.mode import MODE
from setting import CLIENT


async def shuffle(message: discord.Message):
    """
    Setting up the shuffle mode to the music player in the guild.
    """
    guild: discord.Guild = message.guild or message.author.guild
      
    Player.get(guild).set_mode(MODE.SHUFFLE)
    await message.channel.send('Mode: Shuffle activeted !')

CLIENT.add_command(["shuffle"], shuffle)
