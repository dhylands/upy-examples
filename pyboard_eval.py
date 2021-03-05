#!/usr/bin/env python3

import inspect
import pyboard

pyb = pyboard.Pyboard('/dev/cu.usbmodem3389337E34332')

def remote(func):
    def wrapper(*args, **kwargs):
        return do_remote(func, *args, **kwargs)
    return wrapper

def do_remote(func, *args, **kwargs):
    func_name = func.__name__
    func_src = inspect.getsource(func).replace('@remote\n', '')
    args_arr = [repr(i) for i in args]
    kwargs_arr = ["{}={}".format(k, repr(v)) for k, v in kwargs.items()]
    func_src += 'print(repr(' + func_name + '(' + ', '.join(args_arr + kwargs_arr) + ')))\n'
    pyb.enter_raw_repl()
    output = pyb.exec(func_src)
    pyb.exit_raw_repl()
    return eval(output)

@remote
def foo(x):
  return x * 2

@remote
def sysname():
  import os
  return os.uname().sysname

print('sysname =', sysname())
print('foo(4) =', foo(4))
