from __future__ import absolute_import
from mfb2.utils.cache import get_cache_instance
import socket
import json
import logging
logger = logging.getLogger(__name__)


BUFFER = 8192
SERVER = ('localhost', 8809)


def handle_connection(connection):
    try:
            data = connection.recv(BUFFER)
            if data:
                request = json.loads(data)
                logger.info('received request: %s', request)
                ret = process_request(request)
                logger.info('returning ret: %s', ret)
                connection.sendall(json.dumps(ret))
    except:
        logger.error("Error while processing request.", exc_inf=True)
    finally:
        connection.close()


def process_request(request):
    func = request['func'], args = request['args'], kwargs = request['kwargs']
    if func == 'cache.get':
        f = get_cache_instance().__getitem__
    elif func == 'cache.put':
        f = get_cache_instance().put
    elif func == 'cache.contains':
        f = get_cache_instance().__contains__
    else:
        f = None
    return f(*args, **kwargs)


def send_request(func, *args, **kwargs):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER)
    try:

        # Send data
        message = {'func': func, 'args': args, 'kwargs': kwargs}
        sock.sendall(json.dumps(message))

        data = sock.recv(BUFFER)
        return json.loads(data)

    finally:
        sock.close()


def server(monitor=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(SERVER)
        sock.listen(1)
        logger.info('listening on %s', SERVER)

        while monitor is None or not monitor.abortRequested():
            # Wait for a connection
            connection, client_address = sock.accept()
            handle_connection(connection)

    except:
        logger.error('', exc_info=True)
