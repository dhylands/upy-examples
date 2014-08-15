from __future__ import print_function

import sys

def term_size():
    """Print out a sequence of ANSI escape code which will report back the
    size of the window.
    """
    # ESC 7         - Save cursor position
    # ESC 8         - Restore cursor position
    # ESC [r        - Enable scrolling for entire display
    # ESC [row;colH - Move to cursor position
    # ESC [6n       - Device Status Report - send ESC [row;colR
    sys.stdout.write('\x1b7\x1b[r\x1b[999;999H\x1b[6n')
    sys.stdout.flush()
    pos = ''
    while True:
        char = sys.stdin.read(1)
        if char == 'R':
            break
        if char != '\x1b' and char != '[':
            pos += char
    (height, width) = [int(i) for i in pos.split(';')]
    sys.stdout.write('\x1b8')
    sys.stdout.flush()
    return height, width

(height, width) = term_size()
print("height =", height, 'width =', width)
