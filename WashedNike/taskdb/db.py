import multiprocessing
import time
from taskdb.task import Task

class TaskDB(object):
    def __init__(self):
        self.tasks = {}
        self.lock = multiprocessing.Lock()

    def add_task(self, task_id, function, arguments):
        self.tasks[task_id] = Task(task_id, function, arguments)
        return self.tasks[task_id]

    def monitor_task(self, task_id, function, arguments):
        with self.lock:
            task = self.tasks.get(task_id, None)
            if not task:
                task = self.add_task(task_id, function, arguments)
            if not task.active:
                task.start()
            task.watchers += 1

        data = None
        while not data:
            data = task.get_data()
            time.sleep(0.01)

        with self.lock:
            task.watchers -= 1
            if task.watchers == 0:
                task.stop()
        return data
