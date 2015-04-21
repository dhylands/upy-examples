#
# Example which shows how to use readinto.
#

# First we'll populate a file with some data

filename = 'test.txt'

with open(filename, 'wb') as f:
    for i in range(10):
        f.write('{:4d}'.format(i))

print("Read back the file using read")

with open(filename, 'rb') as f:
    while True:
        buf = f.read(4)
        print("buf = '{:s}'".format(buf))
        if not buf:
            break

print("Read back the file using readinto")

with open(filename, 'rb') as f:
    buf = bytearray(10)
    while True:
        len = f.readinto(buf, 4)
        print("buf = '{:s}'".format(str(buf[:len], 'utf-8')))
        if len == 0:
            break

