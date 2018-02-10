import threading
import time
from taskdb.db import TaskDB

class Bot(object):
    def __init__(self):
        self.task_db = TaskDB()
        self.tasks = {}

    def execute_task(self, task):
        raise NotImplementedError('Task execution not implemented')

    def __execute_task_wrapper(self, task):
        self.execute_task(task)

    def start_task(self, task_id):
        task = self.tasks.get(task_id, None)
        if task:
            task.process = threading.Thread(target=self.__execute_task_wrapper, args=(task,))
            task.process.start()

    def stop_task(self, task_id):
        task = self.tasks[task_id]
        if task:
            task.process.terminate()

    def start_multiple_tasks(self, task_ids):
        for task_id in task_ids:
            self.start_task(task_id)

    def stop_multiple_tasks(self, task_ids):
        for task_id in task_ids:
            self.stop_task(task_id)

    def start_all_tasks(self):
        self.start_multiple_tasks(self.tasks)

    def stop_all_tasks(self):
        self.stop_multiple_tasks(self.tasks)

    def add_task(self, task):
        self.tasks[task.id] = task

    def remove_task(self, task_id):
        task = self.tasks.pop(task_id, None)
        if task and task.is_active():
            self.stop_task(task)

    @staticmethod
    def wait_until_time(timestamp):
        while time.time() < timestamp:
            time.sleep(0.01)
