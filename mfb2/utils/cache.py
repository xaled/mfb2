import time
import json
import os

DEFAULT_CACHE_TIMEOUT = 3600
CLEANUP_INTERVAL = 600
OUTPUT_JSON = "mdb2-cache.json"
_cache_instance = None


def get_cache_instance():
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = Cache()
    return _cache_instance


class Cache:
    def __init__(self):
        self.next_cleanup = int(time.time()) + CLEANUP_INTERVAL
        self.db = {}
        if os.path.exists(OUTPUT_JSON):
            with open(OUTPUT_JSON) as fin:
                self.db = json.load(fin)
        else:
            with open(OUTPUT_JSON, 'w') as fou:
                json.dump({}, fou)

    def __getitem__(self, key):
        self._cleanup()
        if key in self.db and int(time.time()) > self.db[key]['expire']:
            del self.db[key]
        return self.db[key]['value']

    def __setitem__(self, key, value):
        self.put(key, value)

    def put(self, key, value, timeout=None):
        self._cleanup()
        self.db[key] = {'value': value, 'requests': 0, 'expire': int(time.time()) + (timeout or DEFAULT_CACHE_TIMEOUT)}

    def __contains__(self, key):
        self._cleanup()
        if key in self.db:
            if int(time.time()) > self.db[key]['expire'] :
                del self.db[key]
                return False
            return True
        return False

    def __delitem__(self, key):
        self._cleanup()
        if key in self.db:
            del self.db[key]

    def _cleanup(self):
        if time.time() > self.next_cleanup:
            to_remove = list()
            t = int(time.time())
            for key in self.db:
                if t > self.db[key].expire:
                    to_remove.append(key)
            for key in to_remove:
                del self.db[key]

            with open(OUTPUT_JSON, 'w') as fou:
                json.dump(self.db, OUTPUT_JSON)
            self.next_cleanup = int(time.time()) + CLEANUP_INTERVAL

