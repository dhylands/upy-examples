#!/usr/bin/env python3

from pyboard import Pyboard
from serial.tools import list_ports
import inspect
import time

DEBUG = False

def remote(pyb, func, *args, **kwargs):
    """Calls func with the indicated args on the micropython board."""
    args_arr = [repr(i) for i in args]
    kwargs_arr = ["{}={}".format(k, repr(v)) for k, v in kwargs.items()]
    func_str = inspect.getsource(func)
    func_str += 'output = ' + func.__name__ + '('
    func_str += ', '.join(args_arr + kwargs_arr)
    func_str += ')\n'
    func_str += 'if output is None:\n'
    func_str += '    print("None")\n'
    func_str += 'else:\n'
    func_str += '    print(output)\n'
    if DEBUG:
        print('----- About to send %d bytes of code to the pyboard -----' % len(func_str))
        print(func_str)
        print('-----')
    pyb.enter_raw_repl()
    output, _ = pyb.exec_raw(func_str)
    pyb.exit_raw_repl()
    if DEBUG:
        print('-----Response-----')
        print(output)
        print('-----')
    return output


def sync_time(pyb):
    now = time.localtime(time.time())
    remote(pyb, set_time, (now.tm_year, now.tm_mon, now.tm_mday, now.tm_wday + 1,
                           now.tm_hour, now.tm_min, now.tm_sec, 0))

def set_time(rtc_time):
    import pyb
    rtc = pyb.RTC()
    rtc.datetime(rtc_time)

def get_time():
    import time
    now = time.localtime(time.time())
    return 'Current pyboard time is {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
            now[0], now[1], now[2], now[3], now[4], now[5])

def find_pyboard():
    for port in list_ports.comports():
        if port.vid == 0xf055 and port.pid >= 0x9800 and port.pid <= 0x9802:
            return port.device

def main():
    pyb_device = find_pyboard()
    if not pyb_device:
        print('Unable to find pyboard')
        return
    pyb = Pyboard(pyb_device)
    sync_time(pyb)
    print(str(remote(pyb, get_time), encoding='utf8').strip())

if __name__ == "__main__":
    main()
