import discord

from models.threads import Player


async def stop(client: discord.Client, message: discord.Message):
    """
    Stop the music of your current Guild
    :param client: Client discord
    :param message: discord.Message
    """
    guild = message.guild or message.author.guild
    
    p = Player.get(guild)
    p.clear_queue()
