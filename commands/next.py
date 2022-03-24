import discord

from setting import CLIENT


async def next(message: discord.Message):
    """
    pass the music of your current Guild

    :param message:
    """
    voice_client: discord.VoiceClient = discord.utils.get(CLIENT.voice_clients, guild=message.guild)
    if not voice_client:
        return
    if voice_client.is_playing():
        voice_client.stop()
