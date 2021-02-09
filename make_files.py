#!/usr/bin/env python3

import binascii
import os
import sys

PREFIX = b"""import binascii
BUFFER_SIZE = 512
FILE_LIST = [
"""

SUFFIX = b"""]

for file in FILE_LIST:
    filename = file['filename']
    print('filename =', filename)
    data = binascii.unhexlify(file['data'])

    print('len(data) =', len(data))
    with open(filename, 'wb') as f:
        bytes_remaining = len(data)
        data_idx = 0
        while bytes_remaining > 0:
            buf_size = min(bytes_remaining, BUFFER_SIZE)
            f.write(data[data_idx:data_idx + buf_size])
            data_idx += buf_size
            bytes_remaining -= buf_size
"""


def main():
    filenames = sys.argv[1:]
    with open('files.py', 'wb') as f:
        f.write(PREFIX)
        for filename in filenames:
            basename = os.path.basename(filename)
            print('filename =', basename)
            with open(filename, 'rb') as src:
                data = src.read()
                hex_data = binascii.hexlify(data)
                f.write("{{'filename': '{}', 'data': {}}},\n".format(basename, hex_data).encode('utf-8'))
        f.write(SUFFIX)

main()
