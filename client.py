import logging
# essential for setting up events
from events import *

from setting import CLIENT, TOKEN

# setting up logging
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s -- %(name)s  -- %(levelname)s -- %(message)s')

CLIENT.run(TOKEN)
