import sys

def bar():
    return 1 / 0

def foo():
    try:
        bar()
    except Exception as err:
        print("Recording error")
        sys.print_exception(err, log_file)
        log_file.flush()

log_file = open('/flash/log.txt', 'w')
print('Test', file=log_file)

foo()


