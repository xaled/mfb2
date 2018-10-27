import xbmc
from mfb2.api import server
import logging
logger = logging.getLogger('service.py')

if __name__ == '__main__':

    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        server(monitor)