import os
import discord

CLIENT = discord.Client()
TOKEN = os.environ.get('TOKEN') or ''
if TOKEN == '':
    print('TOKEN is not set in venv/bin/activate')
    exit()
