import discord

from setting import CLIENT, voice_queue


async def stop(message: discord.Message):
    voice_client: discord.VoiceClient = discord.utils.get(CLIENT.voice_clients, guild=message.guild)
    if not voice_client:
        return
    if voice_client.is_playing():
        try:
            voice_queue[message.guild]['queue'].clear()
        except Exception:
            print('TROP BIZZARE')
        voice_client.stop()
