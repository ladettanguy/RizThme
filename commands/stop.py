import os
import subprocess

import discord

from models import Player


async def stop(message: discord.Message):
    """
    Stop the music of your current Guild
    :param message: discord.Message
    """
    Player.stop_music(message)

    # kill the current process because discord.py API don't make it after disconnected
    # I know that's not a good solution. Contact tamikata#2214 if you have another solution.
    subprocess.run(f'kill -9 {os.getpid()}', shell=True)
