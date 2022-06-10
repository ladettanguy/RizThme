import logging
from ..setting import CLIENT, TOKEN


@CLIENT.event
async def on_disconnect():
    """
    this event run after the server disconnect the client.

    It's used to relogin CLIENT.
    """
    logging.info('Client down!')
    await CLIENT.login(TOKEN)
    logging.info('Client up!')
