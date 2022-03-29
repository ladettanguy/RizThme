import os
import logging

from setting import CLIENT, TOKEN
from models import Player

logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s -- %(name)s  -- %(levelname)s -- %(message)s')


@CLIENT.event
async def on_ready():
    """
    On_ready event run after the client connection is established and the login is successful.

    It's used to set up differents settings and variables.
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
    On_ready event run after the server disconnect the client.

    It's used to relogin CLIENT.
    """
    logging.info('Client down!')
    await CLIENT.login(TOKEN)

CLIENT.run(TOKEN)
