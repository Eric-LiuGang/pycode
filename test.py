# taskmanager.py
import random, time, Queue
from multiprocessing.managers import BaseManager

task_queue = Queue.Queue()
result_queue = Queue.Queue()

class QueueManager(BaseManager):
    pass

QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
manager = QueueManager(address=('192.168.52.129', 5000), authkey='')
manager.start()
task = manager.get_task_queue()
result = manager.get_result_queue()
for i in range(10):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)
print('Try get results...')
for i in range(10):
    r = result.get(timeout=100)
    print('Result: %s' % r)
manager.shutdown()
