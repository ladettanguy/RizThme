import discord
from pytube import YouTube

from setting.config import CLIENT

"""
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
"""


async def play(message: discord.Message):
    voice_channel: discord.VoiceChannel = discord.utils.get(message.guild.voice_channels, name="Général")
    voice_client = discord.utils.get(CLIENT.voice_clients, guild=message.guild)
    print(voice_client)
    url = message.content.split(' ')[1]

    if not voice_client:
        coro = voice_channel.connect()
        voice_client = await coro
    if not voice_client.is_playing():
        ytb: YouTube = YouTube(url)
        audio = ytb.streams[0]
        # Todo changer le stream pour le jouer
        voice_client.play(discord.FFmpegPCMAudio(audio))
