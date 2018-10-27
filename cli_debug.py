from __future__ import absolute_import, print_function, unicode_literals
from mfb2.utils.path import decode_path
from mfb2.utils.addons import get_providers
import logging
import sys
logger = logging.getLogger(__name__)


def cli_debug_shell():
    query = '/'
    while query != 'quit':
        try:
            path, params = query.split()
        except:
            path, params = query, ""

        result = process_query(path, params)
        for r in result:
            print(r)
        query = input('$ ')


def cli_debug_main():
    logging.basicConfig()
    path = '/' if len(sys.argv) < 2 else sys.argv[1]
    params = '' if len(sys.argv) < 3 else sys.argv[2]
    result = process_query(path, params)
    for r in result:
        print(r)


def process_query(path, params):
    path_elements, arguments = decode_path(path, params)

    if len(path_elements) == 0:
        return index()
    else:
        provider_name = path_elements[0]
        provider = load_provider(provider_name)
        node1 = path_elements[1] if len(path_elements) > 1 else '/'
        return provider.process_page(node1, *path_elements[2:], **arguments)


def load_provider(provider_name):
    return get_providers(path='providers')[provider_name]()


def index():
    return get_providers(path='providers').keys()


if __name__ == '__main__':
    cli_debug_main()