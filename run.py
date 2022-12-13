import logging

from rizthme.setting.config import TOKEN
from rizthme.client import Client

logging.basicConfig(filename='log.log', filemode='w', level="INFO",
                    format='%(asctime)s -- %(name)s  -- %(levelname)s -- %(message)s', force=True)

CLIENT = Client()
CLIENT.run(TOKEN)
