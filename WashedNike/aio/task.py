import uuid
import multiprocess
from aio.utilities import *


class Task(object):
    def __init__(self, task_data={}):
        self.id = str(uuid.uuid4())
        self.data = task_data
        self.process = None
        manager = multiprocess.Manager()
        self.status_dict = manager.dict()
        self.set_status('')
        self.logs = manager.list()
        self.logger = utilities.create_logger(self.id)

    def is_active(self):
        return self.process is not None and self.process.is_alive()

    def set_status(self, status):
        self.status_dict['status'] = status

    def get_status(self):
        return self.status_dict['status']

    def log(self, info):
        self.logs.append(info)
        self.logger.info(info)

    def get_logs(self):
        return self.logs