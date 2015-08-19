from . import Storage

class RedisStorage(Storage):
    '''
    Storage class for redis.

    Config:
        expiry: number of seconds before expiring task, 0 to disable (default: 0)
    '''

    default_config = {
        'expiry': 0,
    }

    def get(self, key):
        return self.connection.get(key)

    def obtain_lock(self, key, value):
        obtained = self.connection.setnx(key, value)
        if self.config['expiry'] and obtained:
            self.connection.expire(key, self.config['expiry'])

        return obtained

    def release_lock(self, key):
        self.connection.delete(key)
