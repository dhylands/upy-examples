import sys
import io

output = io.StringIO()

def bar():
    return 1 / 0

def foo():
    try:
        bar()
    except Exception as err:
        print("Recording error")
        sys.print_exception(err, output)
        print('output = ', output.getvalue())

foo()


