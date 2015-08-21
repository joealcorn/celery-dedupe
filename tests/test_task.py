from celery import current_app
from celery.task import task
from redis import StrictRedis

from celery_dedupe import DedupeTask
from celery_dedupe.storage.redis import RedisStorage
from tests import settings

redis = StrictRedis(db=9)
storage = RedisStorage(redis, expiry=60)


@task(base=DedupeTask, storage=storage)
def noop_task(*a, **kw):
    return None


@task(base=DedupeTask, storage=storage)
def raise_exception(*a, **kw):
    raise AttributeError()


class TestDedupeTask(object):

    def setup_class(self):
        current_app.config_from_object(settings)

    def test_create_key(self):
        task = DedupeTask()

        key = task._create_key(tuple(), {})
        assert key == 'cd:celery_dedupe.tasks.DedupeTask:d41d8cd98f00b204e9800998ecf8427e'

        key = task._create_key((True, False), {})
        assert key == 'cd:celery_dedupe.tasks.DedupeTask:85eadac9a27eb1f6dccf00145df6003b'

        key = task._create_key(tuple(), {'something': 2})
        assert key == 'cd:celery_dedupe.tasks.DedupeTask:a758dbbdf7ba75fc39732ab4cca53049'

        key = task._create_key(tuple(), {'something_else': 2})
        assert key == 'cd:celery_dedupe.tasks.DedupeTask:271a7d4a14d7892b87b8fc96d50507a9'

    def test_apply_task_twice(self):
        result1 = noop_task.apply_async(countdown=10)
        result2 = noop_task.apply_async()
        assert result1.task_id == result2.task_id

    def test_apply_task_once(self):
        result = noop_task.delay(1)
        assert result.get() == None

    def test_key_cleared_on_exception(self):
        key = raise_exception._create_key(tuple(), dict())
        assert not redis.exists(key)
        try:
            raise_exception.delay().get()
        except AttributeError:
            pass

        assert not redis.exists(key)
