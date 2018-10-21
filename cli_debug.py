from __future__ import absolute_import, print_function, unicode_literals
from mfb2.utils.path import decode_path


def cli_debug_main():
    query = '/'
    while query != 'quit':
        result = process_query(query)
        for r in result:
            print(r.__dict__)
        query = input('$ ')


def process_query(query):
    try:
        path, params = query.split()
    except:
        path, params = query, ""

    path_elements, arguments = decode_path(path, params)

    if len(path_elements) == 0:
        return index()
    else:
        provider_name = path_elements[0]
        provider = load_provider(provider_name)
        node1 = path_elements[1] if len(path_elements) > 1 else '/'
        return provider.process_page(node1, *path_elements[2:], **arguments)


def load_provider(provider_name):
    if provider_name == 'gogoanime':
        from providers.gogoanime import GogonanimeProvider
        return GogonanimeProvider()


def index():
    return []


if __name__ == '__main__':
    cli_debug_main()