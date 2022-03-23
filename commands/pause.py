import discord

from models import Player


async def pause(message: discord.Message):  # sourcery skip: use-named-expression
    """

    :param message:
    :return:
    """
    guild: discord.Guild = message.guild
    player: Player = Player.voice_thread.get(guild)
