class MyTimeoutException(Exception):

    def __init__(self,id):
        self.id = id

    def __str__(self):
        print("task:" + str(self.id) + ",timeout!")


class CanceledException(Exception):

    def __init__(self,id):
        self.id = id

    def __str__(self):
        print("task:" + str(self.id) + ",canceled!")

class ArgsErrorException(Exception):
    
    def __init__(self):
        print("submit args must bigger than 0")