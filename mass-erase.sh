#!/bin/sh
#
# This script demonstates how to mass-erase the entire flash.

set -x

echo -e -n "\xff" > ff.bin
dfu-util -s :mass-erase:force -a 0 -d 0483:df11 -D ff.bin
