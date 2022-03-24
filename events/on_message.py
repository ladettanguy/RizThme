import discord

from events import CLIENT
from commands import commands


@CLIENT.event
async def on_message(message: discord.Message):
    """
    On_message event run for each message from Guild or Private Channel
    :param message: discord.Message
    """
    cmd_line = message.content.split(' ')
    # Cut the content for get the principal command
    cmd: str = cmd_line[0]
    cmd = cmd.replace('!', '')
    if cmd in commands:
        print(f"la commande : {cmd}, by {message.author}")
        func = commands[cmd]
        # Call the appropriate for the command wanted and pass the discord.Message in parameters
        await func(message)
