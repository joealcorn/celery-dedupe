# celery-dedupe [![Build Status](https://travis-ci.org/joealcorn/celery-dedupe.svg?branch=master)](https://travis-ci.org/joealcorn/celery-dedupe)

celery-dedupe is a project that aims to be a pluggable solution for deduplicating queued celery tasks.
Only redis is supported as a storage backend for the moment.

# Usage

```python
from celery.task import task
from celery_dedupe import DedupeTask
from celery_dedupe.storage.redis import RedisStorage
from redis import StrictRedis

redis = StrictRedis()
storage = RedisStorage(redis, expiry=60)

@task(base=DedupeTask, storage=storage)
def noop_task(*a, **kw):
    return None
```


# Caveats and things to watch out for

#### CELERY_ALWAYS_EAGER can not return results

Any subsequent invocation of a task when `CELERY_ALWAYS_EAGER` is set to `True` is unable to return
an `EagerResult` object.


#### Unacknowledged tasks

Any unacked tasks will not be able to be requeued by usual means.
Setting an expiry on the redis storage backend will allow you to work around this if it's not vital
that multiple tasks are queued at once.


#### Manually purging your broker

If you need to manually consume tasks or completely purge your broker for whatever reason you'll
need to remove the corresponding keys from your storage backend as well so that tasks can continue
to run.


#### Tasks with ETAs, countdowns or retry delays

Any task with a delayed start time will prevent other tasks from running immediately. If a task
retries many times with an exponential backoff this can be a long period of time. The key expiry
on the redis backend can minimise the effect of this.


#### Unregistered tasks

If you somehow queue an unregistered task (most likely during development), you will not be able
to requeue even when registered without clearing the lock from your storage backend
