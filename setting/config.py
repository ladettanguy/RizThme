import os
import discord

CLIENT = discord.Client()
TOKEN = os.getenv('TOKEN')
if TOKEN is None:
    print('TOKEN is not set in venv/bin/activate')
    exit()
