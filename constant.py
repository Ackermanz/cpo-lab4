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