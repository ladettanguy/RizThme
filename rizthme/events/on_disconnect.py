import logging
from rizthme.setting.config import TOKEN


def init(client: "Client"):

    @client.event
    async def on_disconnect():
        """
        this event run after the server disconnect the client.

        It's used to relogin CLIENT.
        """
        logging.info('Client down!')
        await client.login(TOKEN)
        logging.info('Client up!')
