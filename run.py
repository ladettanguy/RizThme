import logging

from setting.config import TOKEN
from setting.client import Client

logging.basicConfig(filename='log.log', filemode='w', level="INFO",
                    format='%(asctime)s -- %(name)s  -- %(levelname)s -- %(message)s', force=True)

CLIENT = Client()
CLIENT.setup()
print(CLIENT.commands)
CLIENT.run(TOKEN)
