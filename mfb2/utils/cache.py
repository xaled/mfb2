import time


CACHE_TIMEOUT = 3600


class Cache:
    def __init__(self):
        self.db = dict()
        self.last_cleanup = 0

    def __getitem__(self, key):
        if key in self.db and int(time.time()) - self.db[key]['timestamp'] > CACHE_TIMEOUT:
            del self.db[key]
        return self.db[key]['value']

    def __putitem__(self, key, value):
        self.db[key] = {'value': value, 'timestamp': int(time.time())}

    def __contains__(self, key):
        if key in self.db:
            if int(time.time()) - self.db[key]['timestamp'] > CACHE_TIMEOUT:
                del self.db[key]
                return False
            return True
        return False

    def __delitem__(self, key):
        if key in self.db:
            del self.db[key]
