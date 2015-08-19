from uuid import uuid4
from redis import StrictRedis

from celery_dedupe.storage.redis import RedisStorage

class TestRedisStorage(object):

    @property
    def redis(self):
        if hasattr(self, '_redis'):
            return self._redis

        self._redis = StrictRedis()
        return self._redis

    def test_lock_obtained(self):
        storage = RedisStorage(self.redis)
        assert storage.obtain_lock(uuid4(), '1')

    def test_lock_obtained_with_expiry(self):
        key = uuid4()
        storage = RedisStorage(self.redis, expiry=10)
        assert storage.obtain_lock(key, '1')
        assert self.redis.ttl(key) == 10

    def test_already_locked(self):
        key = uuid4()
        self.redis.setex(key, '1', 10)
        storage = RedisStorage(self.redis, expiry=10)
        assert not storage.obtain_lock(key, '1')

    def test_release_lock(self):
        key = uuid4()
        self.redis.setex(key, '1', 10)
        storage = RedisStorage(self.redis, expiry=10)
        storage.release_lock(key)
        assert not self.redis.get(key)
