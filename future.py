import threading
from typing import Optional

from constant import *
from exception import *


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
