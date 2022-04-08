import logging
# essential for setting up events
import events

from setting import CLIENT, TOKEN


logging.basicConfig(filename='log.log', filemode='w', level="INFO",
                    format='%(asctime)s -- %(name)s  -- %(levelname)s -- %(message)s', force=True)

CLIENT.run(TOKEN)
