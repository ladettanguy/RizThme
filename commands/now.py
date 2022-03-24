import discord

from models import Player


async def now(message: discord.Message):  # sourcery skip: use-named-expression
    """
    Send to the same textual channel, the current music playing in this Guild

    :param message: discord.Message
    """
    guild: discord.Guild = message.guild
    if not guild:
        return
    info = Player.get_now_played(guild)
    if info:
        await message.channel.send(f'titre: {info[0]}.\nLien: {info[1]}')
    else:
        await message.channel.send("I'm not playing song")
