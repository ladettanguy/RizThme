import discord
import logging

from setting import CLIENT
from commands import commands, PREFIX


@CLIENT.event
async def on_message(message: discord.Message):
    """
    This event is called when a message is sent in a channel.

    :param message: The message that was sent.
    """
    # Ignore bot messages
    if message.author.bot:
        return
    # Ignore messages without prefix
    if not message.content.startswith(PREFIX):
        return

    # Split message into command and arguments
    cmd_line = message.content.split(' ')
    # Get command
    cmd: str = cmd_line[0]
    cmd = cmd.replace(PREFIX, '')

    # if command is in commands list
    if cmd in commands:
        logging.info(f"la commande : {cmd}, by {message.author}")
        func = commands[cmd]
        # Call the appropriate for the command wanted and pass the discord.Message in parameters
        await func(message)
