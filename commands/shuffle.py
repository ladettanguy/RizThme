import discord

from models.threads import Player
from models.mode import MODE


async def shuffle(client: discord.Client, message: discord.Message):
    """
    Setting up the shuffle mode to the music player in the guild.
    """
    guild: discord.Guild = message.guild or message.author.guild
      
    Player.get(guild).set_mode(MODE.SHUFFLE)
    await message.channel.send('Mode: Shuffle activeted !')

