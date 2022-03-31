import discord

from models import Player


async def stop(message: discord.Message):
    """
    Stop the music of your current Guild
    :param message: discord.Message
    """
    Player.stop_music(message.guild)
