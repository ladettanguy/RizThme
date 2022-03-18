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
    voice = discord.utils.get(CLIENT.voice_clients, guild=message.guild)
    if not voice:
        voice = discord.VoiceClient(CLIENT, voice_channel)
    print(CLIENT.voice_clients)
    print(voice_channel.id == 708312526164721719)
    url = message.content.split(' ')[1]
    if not voice:
        return
    if not voice.is_connected():
        await voice_channel.connect()
    if not voice.is_playing():
        print(url)
        ytb: YouTube = YouTube(url)
        audio = ytb.streams[0]
        print(type(audio))
        await voice.play(audio)
