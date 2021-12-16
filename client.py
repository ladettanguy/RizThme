import os
from setting.config import CLIENT, TOKEN


@CLIENT.event
async def on_ready():
    os.chdir('./events')
    list_file = os.listdir()
    list_file.remove('__init__.py')
    for filename in list_file:
        __import__(f'events.{filename.split(".")[0]}')
    os.chdir('..')


CLIENT.run(TOKEN)
