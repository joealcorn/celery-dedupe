# celery-dedupe [![Build Status](https://travis-ci.org/joealcorn/celery-dedupe.svg?branch=master)](https://travis-ci.org/joealcorn/celery-dedupe)

celery-dedupe is a project that aims to be a pluggable solution for deduplicating queued celery tasks


# Things to look out for

- Tasks with an ETA or countdown
- Unregistered tasks
- Unacknowledged tasks
- Manually purging your broker
- CELERY_ALWAYS_EAGER can not return a result
