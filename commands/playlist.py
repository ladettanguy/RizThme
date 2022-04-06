import asyncio
from typing import Union

import discord

from models import Player
from setting import CLIENT


async def playlist(message: discord.Message) -> None:
    """
    plays music playlist in the voice channel of the user who wrote the command.

    The command allows playing YouTube links and play audio without downloading the video.

    :param message: discord.Message, message sent by the user wanting to launch music
    """
    guild: discord.Guild = message.guild or message.author.guild

    # Retrieves the bot's VoiceClient, if there is already one present in the server.
    voice_client = discord.utils.get(CLIENT.voice_clients, guild=guild)
    if not voice_client:
        # Recover the voice channel of the message author.
        voice_channel: discord.VoiceChannel = message.author.voice.channel
        # if not, connect (by creating) to the server with a discord.VoiceClient
        voice_client: Union[discord.VoiceClient, discord.VoiceProtocol] = await voice_channel.connect()
        # Set the new VoiceClient to the appropriate thread
        Player.set_voice_client(guild, voice_client)

    await message.channel.send("Loading playlist... (this may take a while)")

    # Call Player, to add playlist
    asyncio.run_coroutine_threadsafe(Player.add_playlist(message), asyncio.get_event_loop())
