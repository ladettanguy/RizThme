import logging

import discord

from setting.config import TOKEN


async def on_disconnect(client: discord.Client):
    """
    this event run after the server disconnect the client.

    It's used to relogin CLIENT.
    """
    logging.info('Client down!')
    await client.login(TOKEN)
    logging.info('Client up!')
