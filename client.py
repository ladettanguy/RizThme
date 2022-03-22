import os
from setting import CLIENT, TOKEN, setup_music_queue


@CLIENT.event
async def on_ready():
    # Setup le dictionnaire de music queue
    setup_music_queue()

    # Import les différents event du dossier events
    os.chdir('./events')
    list_file = os.listdir()
    list_file.remove('__init__.py')
    for filename in list_file:
        __import__(f'events.{filename.split(".")[0]}')
    os.chdir('..')

    print("Client prêt !")


CLIENT.run(TOKEN)
