from __future__ import absolute_import
from mfb2.provider import AbstractProvider
from mfb2.resolver import AbstractResolver
import imp
import time
import os


ADDON_PATH = ""
RELOAD_ADDONS_INTERVAL = 3600
_last_load = 0.0
_providers = None
_resolvers = None


def _reload_addon(path=ADDON_PATH):
    global _providers, _resolvers, _last_load
    _providers = dict() # TODO core provider & resolvers
    _resolvers = dict()
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            filepath = os.path.join(path, filename)
            module_ = imp.load_source('mfb2.ext.' + filename[:-4], filepath)
            for key in dir(module_):
                value = getattr(module_, key)
                if isinstance(value, type):
                    if issubclass(value, AbstractProvider):
                        _providers[key] = value
                    elif issubclass(value, AbstractResolver):
                        _resolvers[key] = value
    _last_load = time.time()


def get_providers(path=ADDON_PATH, force_reload=False):
    if force_reload or time.time() - _last_load > RELOAD_ADDONS_INTERVAL:
        _reload_addon(path)
    return _providers


def get_resolvers(path=ADDON_PATH, force_reload=False):
    if force_reload or time.time() - _last_load > RELOAD_ADDONS_INTERVAL:
        _reload_addon(path)
    return _resolvers
