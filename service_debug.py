from mfb2.api import server
import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    server()
