#!/bin/sh
#
# This script demonstates how to erase just the filesystem on a pyboard.
#
# It actually only erases the first sector of the filesystem, but this
# is enough to make micropython reinitialize things.

set -x

echo -e -n "\xff" > ff.bin
dfu-util -s 0x08004000:leave -a 0 -d 0483:df11 -D ff.bin
