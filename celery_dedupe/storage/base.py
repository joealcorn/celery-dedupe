class Storage(object):
    '''
    Defines the public api for Storages
    '''

    default_config = {}

    def __init__(self, connection, **config):
        self.connection = connection
        self.config = self.default_config.copy()
        self.config.update(config)

    def obtain_lock(self, key, value):
        '''
        Responsible for obtaining a lock for the task
        :returns boolean: Whether lock could be obtained or not
        '''
        raise NotImplementedError
