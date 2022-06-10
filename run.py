import asyncio
import logging

# essential for setting up events
from . import events
# essential for setting up the client commands
from . import commands


from .setting import CLIENT, TOKEN


logging.basicConfig(filename='log.log', filemode='w', level="INFO",
                    format='%(asctime)s -- %(name)s  -- %(levelname)s -- %(message)s', force=True)

CLIENT.run(TOKEN, loop=asyncio.get_event_loop())
