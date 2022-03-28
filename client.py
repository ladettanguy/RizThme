import os
import subprocess
import logging

from setting import CLIENT, TOKEN
from models import Player

logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')


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

    logging.info('Client ready!')


@CLIENT.event
async def on_disconnect():
    """
    On_ready event run after the client close the connection.

    It's used to make a shell command to kill the process
    """
    logging.info('Client down!')

    # kill the current process because discord.py API don't make it after disconnected
    # I know that's not a good solution. Contact tamikata#2214 if you have another solution.
    subprocess.run(f'kill -9 {os.getpid()}', shell=True)


CLIENT.run(TOKEN)
