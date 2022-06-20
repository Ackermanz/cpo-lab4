from constant import *
from exception import *
from future import *

class WorkItem(object):
    def __init__(self,future:Future,fn,args:list,priority=MIN_PRIORITY)->None:
        self.future = future
        self.fn = fn
        self.args = args
        self.priority = priority

    def run(self)->None:
        self.future.setState(RUNNING)
        if self.args is not None:
            result = self.fn(*self.args)
        else:
            result = self.fn()
        self.future.setResult(result)

    def setPriority(self,priority:int)->None:
        self.priority = priority

    def __lt__(self, other):
        return self.priority > other.priority