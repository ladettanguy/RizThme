import discord

from ..setting import CLIENT


async def resume(message: discord.Message):  # sourcery skip: use-named-expression
    """
    Pause the music of your current Guild

    :param message: discord.Message
    """
    guild: discord.Guild = message.guild or message.author.guild

    # Retrieves the bot's VoiceClient, if there is already one present in the server.
    voice_client: discord.VoiceClient = discord.utils.get(CLIENT.voice_clients, guild=guild)
    if not voice_client:
        return

    if voice_client.is_paused():
        voice_client.resume()
        await message.channel.send("Music resumed.")

CLIENT.add_command(["resume"], resume)
