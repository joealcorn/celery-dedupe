import hashlib
import logging
import warnings

from celery import Task
from celery.result import EagerResult
from celery.utils import uuid

logger = logging.getLogger('celery_dedupe')


class DedupeTask(Task):
    abtract = True
    storage = None

    def apply_async(self, args=None, kwargs=None, **kw):
        key = self._create_key(args, kwargs)
        task_id = kw.setdefault('task_id', uuid())

        if self.storage.obtain_lock(key, task_id):
            logger.debug('Queueing %s [%s]', task_id, key)
            return super(DedupeTask, self).apply_async(args=args, kwargs=kwargs, **kw)

        existing_task_id = self.storage.get(key)
        if existing_task_id == task_id:
            # This should be a retry, so add it to the broker anyway
            logger.debug('Queueing %s for retry [%s]', task_id, key)
            return super(DedupeTask, self).apply_async(args=args, kwargs=kwargs, **kw)

        app = self._get_app()
        if app.conf.CELERY_ALWAYS_EAGER:
            warnings.warn('Using DedupeTask in conjunction with CELERY_ALWAYS_EAGER, can not return EagerResult')

        logger.debug('%s already queued, returning AsyncResult [%s]', task_id, key)
        return self.AsyncResult(existing_task_id)

    def on_success(self, retval, task_id, args, kwargs):
        key = self._create_key(args, kwargs)
        self.storage.release_lock(key)

    def on_failure(self, exception, task_id, args, kwargs, einfo):
        key = self._create_key(args, kwargs)
        self.storage.release_lock(key)

    def _create_key(self, args, kwargs):
        args = args or tuple()
        kwargs = kwargs or dict()

        arg_string = ','.join([str(a) for a in args])
        kwarg_string = ','.join(['%s=%s' % (k, v) for k, v in kwargs.iteritems()])
        arg_hash = hashlib.md5(arg_string + kwarg_string).hexdigest()
        import_path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        return 'cd:%s:%s' % (import_path, arg_hash)
