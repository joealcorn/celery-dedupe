# celery-dedupe [![Build Status](https://travis-ci.org/joealcorn/celery-dedupe.svg?branch=master)](https://travis-ci.org/joealcorn/celery-dedupe)

celery-dedupe is a project that aims to be a pluggable solution for deduplicating queued celery tasks

# Usage

```python
from celery.task import task
from celery_dedupe import DedupeTask
from celery_dedupe.storage.redis import RedisStorage
from redis import StricRedit

redis = StrictRedis()
storage = RedisStorage(redis, expiry=60)

@task(base=DedupeTask, storage=storage)
def noop_task(*a, **kw):
    return None
```


# Things to look out for

- Tasks with an ETA or countdown
- Unregistered tasks
- Unacknowledged tasks
- Manually purging your broker
- CELERY_ALWAYS_EAGER can not return a result
