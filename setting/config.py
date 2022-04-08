import os
from setting.client import Client

CLIENT = Client()
TOKEN = os.getenv('TOKEN')
if TOKEN is None:
    print('TOKEN is not set in venv/bin/activate')
    exit()
