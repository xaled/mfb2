from __future__ import unicode_literals
import os
import logging
logger = logging.getLogger(__name__)
try:
    from urllib.parse import urlencode, parse_qsl, urlparse
except ImportError:
    from urlparse import parse_qsl, urlparse
    from urllib import urlencode


def join_path(path_elements):
    path = '/'
    for e in path_elements:
        path = os.path.join(path, e)
    return path


def split_path(path):
    if not path.startswith('/'):
        path = '/' + path
    path_elements = list()
    while path != '/':
        path, child = os.path.split(path)
        path_elements.insert(0, child)
    return path_elements


# def encoded_tuple_list(in_tuple_list):
#     out_list = []
#     for k, v in in_tuple_list:
#         if isinstance(v, unicode):
#             v = v.encode('utf8')
#         elif isinstance(v, str):
#             # Must be encoded in UTF-8
#             v.decode('utf8')
#         out_list.append((k, v))
#     return out_list


def encode_params(**params):
    try:
        qs = urlencode(tuple([(k, params[k]) for k in params.keys() if params[k] is not None]))
        return '' if qs == '' else "?" + qs
    except:
        logger.error("Error encoding params: %s", params, exc_info=True)


def decode_params(param_string):
    if param_string.startswith("?"):
        return dict(parse_qsl(param_string[1:]))
    return {}


def encode_path(path_elements=None, arguments=None):
    arguments = arguments or dict()
    path_elements = path_elements or list()
    return join_path(path_elements) + encode_params(**arguments)


def decode_path(path, args):
    return split_path(path), decode_params(args)