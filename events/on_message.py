import discord

from events import CLIENT
from commands import commands


@CLIENT.event
async def on_message(message: discord.Message):
    cmd_line = message.content.split(' ')
    cmd: str = cmd_line[0]
    cmd = cmd.replace('!', '')
    if cmd in commands:
        print(f"la commande : {cmd}")
        func = commands[cmd]
        await func(message)
