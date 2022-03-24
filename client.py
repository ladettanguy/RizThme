import os
import subprocess
import threading

from setting import CLIENT, TOKEN
from models import Player


@CLIENT.event
async def on_ready():
    """
    On_ready event run after the client connection is established.

    It's used to set up differents settings
    """
    # Setup Players Guild's thread
    Player.setup_music_queue()

    # Setup all differents CLIENT's events
    os.chdir('./events')
    list_file = os.listdir()
    list_file.remove('__init__.py')
    for filename in list_file:
        __import__(f'events.{filename.split(".")[0]}')
    os.chdir('..')

    print("Client ready! \n")


@CLIENT.event
async def on_disconnect():
    """
    On_ready event run after the client close the connection.

    It's used to make a shell command to kill the process
    """
    print("Client down!\n")

    # kill the current process because discord.py API don't make it after disconnected
    # I know that's not a good solution. Contact tamikata#2214 if you have another solution.
    subprocess.run(f'kill -9 {threading.current_thread().native_id}', shell=True)


CLIENT.run(TOKEN)
