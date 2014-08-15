def TaskOne():
    while True:
        # do work
        # relinquish control
        print("Task One!")
        yield None

def TaskTwo():
    while True:
        print("Task Two!")
        yield None

TaskQueue = [ TaskOne(), TaskTwo() ]

while True:
    # main loop here
    for task in TaskQueue:
        next(task)

