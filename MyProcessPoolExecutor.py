import queue
from exception import *
from future import *
from WorkItem import *


def runner(work_queue: queue.PriorityQueue) -> None:
    while True:
        work_item = work_queue.get(block=True)
        if work_item is not None:
            work_item.run()
            work_queue.task_done()
            continue


class MyProcessPoolExecutor(object):
    def __init__(self, max_workers=2) -> None:
        if max_workers <= 0:
            max_workers = 2
        self.max_workers = max_workers
        self.work_queue = queue.PriorityQueue()
        assert isinstance(self.work_queue, queue.PriorityQueue)
        self.threadsSet = set()
        for i in range(max_workers):
            t = threading.Thread(target=runner, args=(self.work_queue,))
            t.daemon = True
            t.start()
            self.threadsSet.add(t)

    def submit(self, *args, priority=MIN_PRIORITY):
        if len(args) == 0:
            raise ArgsErrorException()
        if len(args) == 1:
            fn = args
            args = None
        if len(args) >= 2:
            fn, *args = args
        future = Future()
        item = WorkItem(future, fn, args, priority)
        self.work_queue.put(item)
        return future
