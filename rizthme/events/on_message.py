import asyncio

import discord
import logging


def init(client: "Client"):

    @client.event
    async def on_message(message: discord.Message):
        """
        This event is called when a message is sent in a channel.

        :param message: The message that was sent.
        """
        # Ignore bot messages
        if message.author.bot:
            return

        # Ignore messages without prefix
        if not message.content.startswith(client.PREFIX):
            return

        # Split message into command and arguments
        cmd_line = message.content.split(' ')
        # Get command
        cmd: str = cmd_line[0]
        cmd = cmd.replace(client.PREFIX, '')

        # if command is in commands list
        if cmd in client.commands:
            logging.info(f"la commande : {cmd}, by {message.author}")
            func = client.commands[cmd]
            # Call the appropriate for the command wanted and pass the discord.Message in parameters
            asyncio.run_coroutine_threadsafe(func(message), asyncio.get_event_loop())
