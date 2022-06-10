import discord

from ..models import Player
from ..models.mode import MODE
from ..setting import CLIENT


async def unloop(message: discord.Message):
    """
    Setting up the normal mode to the music player in the guild.
    """
    guild: discord.Guild = message.guild or message.author.guild
    Player.set_mode(guild, MODE.NORMAL)

CLIENT.add_command(["unloop"], unloop)
