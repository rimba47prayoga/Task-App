
class BaseService(object):

    def __init__(self, payload=None):
        self.payload = payload

    def execute(self):
        raise NotImplementedError
