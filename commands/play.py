import os
import discord
from pytube import YouTube
from setting.config import CLIENT
from commands import song_queue


async def play(message: discord.Message):
    # song_there = os.path.isfile("../commands/song.mp3")
    # try:
    #     if song_there:
    #         os.remove("song.mp3")
    # except PermissionError:
    #     await message.channel.send("Attendez que la music actuel soit terminé ou utilisé la commande !stop")
    message.author
    urls = message.content.split(' ')[1::]
    voice_channel: discord.VoiceChannel = discord.utils.get(ctx.guild.voice_channels, name="Général")
    voice: discord.VoiceClient = CLIENT.voice_clients
    if not voice.is_connected():
        await voice_channel.connect()
    for url in urls:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        song_queue.append(audio)
    if not voice.is_playing():
        while len(song_queue) != 0:
            await voice.play(song_queue.pop(0))

    # ydl_opts = {
    #     'format': 'bestaudio/best',
    #     'postprocessors': [{
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192',
    #     }],
    # }
    #
    #
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     os.chdir("../songs")
    #     await ctx.send("The youtube link is downloading ..")
    #     ydl.download([url])
    # os.chdir("../commands")
    #
    # for file in os.listdir('./'):
    #     if file.endswith('.mp3'):
    #         os.rename(file, 'song.mp3')
    # voice.play(discord.FFmpegPCMAudio('song.mp3'))
