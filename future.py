import queue
import threading
from typing import Optional


class Future(object):
    def __init__(self) -> None:
        self.state = PENDING
        self.result = None
        self.condition = threading.Condition()
        self.id = getId()

    def IsDone(self) -> bool:
        return FINISHED == self.state

    def IsProgress(self) -> bool:
        return RUNNING == self.state

    def Result(self, timeout=None) -> Optional[int]:
        with self.condition:
            if self.state == FINISHED:
                return self.result
            elif self.state == CANCELED:
                raise CanceledException(self.id)
            else:
                # if not finished then wait
                self.condition.wait(timeout)
                if self.state == FINISHED:
                    return self.result
                elif self.state == CANCELED:
                    raise CanceledException(self.id)
                else:
                    # means task has timeout
                    raise MyTimeoutException(self.id)

    def Cancel(self) -> bool:
        if self.state != FINISHED and self.state != RUNNING:
            self.setState(CANCELED)
            return True
        else:
            return False

    def setState(self, state: int) -> None:
        self.state = state

    def setResult(self, result: int) -> None:
        with self.condition:
            self.result = result    # type: ignore
            self.setState(FINISHED)
            self.condition.notify_all()


PENDING = 1
RUNNING = 2
FINISHED = 3
CANCELED = 4
MAX_PRIORITY = 10
MIN_PRIORITY = 1

ID = 0


def getId() -> int:
    global ID
    id = ID
    ID += 1
    return id


def resetID() -> None:
    global ID
    ID = 0


class MyTimeoutException(Exception):

    def __init__(self, id):
        self.id = id

    def __str__(self):
        print("task:" + str(self.id) + ",timeout!")


class CanceledException(Exception):

    def __init__(self, id):
        self.id = id

    def __str__(self):
        print("task:" + str(self.id) + ",canceled!")


class ArgsErrorException(Exception):

    def __init__(self):
        print("submit args must bigger than 0")


class WorkItem(object):
    def __init__(
            self,
            future: Future,
            fn,
            args: list,
            priority=MIN_PRIORITY) -> None:
        self.future = future
        self.fn = fn
        self.args = args
        self.priority = priority

    def run(self) -> None:
        self.future.setState(RUNNING)
        if self.args is not None:
            result = self.fn(*self.args)
        else:
            result = self.fn()
        self.future.setResult(result)

    def setPriority(self, priority: int) -> None:
        self.priority = priority

    def __lt__(self, other):
        return self.priority > other.priority


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
        # self.work_queue = queue.Queue()
        self.work_queue = queue.PriorityQueue()  # type: ignore
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
