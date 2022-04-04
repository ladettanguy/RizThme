import logging
# essential for setting up events
import events

from setting import CLIENT, TOKEN

# setting up logging
logging.basicConfig(filename='log.log', level="INFO", format='%(asctime)s -- %(name)s  -- %(levelname)s -- %(message)s')

CLIENT.run(TOKEN)
