import time
import traceback
import multiprocessing

def run_until_complete(target=None, args=(), interval=0.01):
    result = None
    while (not result or (isinstance(result, tuple) and not all(result)) and not (isinstance(result, list) and not result)):
        try:
            result = target(*args)
        except Exception:
            error = traceback.format_exc()
            print(error)
        time.sleep(interval) # Avoid busy waiting
    return result

class Task(object):
    def __init__(self, task_id, function, arguments=()):
        self.task_id = task_id
        self.function = function
        self.arguments = arguments

        self.manager = multiprocessing.Manager()
        self.namespace = self.manager.Namespace()
        self.namespace.data = None
        self.watchers = 0
        self.active = False
        self.process = None

    def execute(self):
        while True:
            self.namespace.data = run_until_complete(target=self.function, args=self.arguments)
            time.sleep(0.01)

    def get_data(self):
        return self.namespace.data

    def start(self):
        self.active = True
        self.process = multiprocessing.Process(target=self.execute)
        self.process.start()

    def stop(self):
        self.active = False
        self.process.terminate()
