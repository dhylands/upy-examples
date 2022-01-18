#
# Script which runs on MicroPython and prints info about
# the filesystem which is currently running.
#
# This was taken from: https://forum.micropython.org/viewtopic.php?p=64410#p64410

"""
Dump info about a filesystem.
"""

import sys, struct

def pr(addr, label, data):
    if type(data) == bytes or type(data) == bytearray:
        data = ':'.join('%02x' % b for b in data)
    print('%04x  %-32s %s' % (addr, label, data))

def decode_bootsec_fat(b):
    print('FAT filesystem')
    pr(0, 'jump', b[0:3])
    pr(3, 'OEM name', str(b[3:11], 'ascii'))
    pr(11, 'sector size (bytes)', struct.unpack_from('<H', b, 11)[0])
    pr(13, 'cluster size (sectors)', struct.unpack_from('<B', b, 13)[0])
    pr(14, 'reserved area (sectors)', struct.unpack_from('<H', b, 14)[0])
    pr(16, 'number of FATs', struct.unpack_from('<B', b, 16)[0])
    pr(17, 'size of root dir area', struct.unpack_from('<H', b, 17)[0])
    pr(19, 'volume size (sectors)', struct.unpack_from('<H', b, 19)[0])
    pr(21, 'media descsriptor', hex(struct.unpack_from('<B', b, 21)[0]))
    pr(22, 'FAT size (sectors)', struct.unpack_from('<H', b, 22)[0])
    pr(24, 'track size (sectors)', struct.unpack_from('<H', b, 24)[0])
    pr(26, 'number of heads', struct.unpack_from('<H', b, 26)[0])
    pr(28, 'volume offset (sectors)', struct.unpack_from('<L', b, 28)[0])
    pr(32, 'volume size (32-bit) (sectors)', struct.unpack_from('<I', b, 32)[0])
    pr(36, 'physical drive number', struct.unpack_from('<B', b, 36)[0])
    pr(37, 'error flag', hex(struct.unpack_from('<B', b, 37)[0]))
    pr(38, 'extended boot signature', hex(struct.unpack_from('<B', b, 38)[0]))
    pr(39, 'volume serial number', hex(struct.unpack_from('<L', b, 39)[0]))
    pr(43, 'volume label', str(b[43:51], 'ascii'))
    pr(54, 'filesystem type', str(b[54:62], 'ascii'))
    pr(510, 'signature', hex(struct.unpack_from('<H', b, 510)[0]))


def decode_bootsec_lfs1(b):
    print("Littlefs v1 filesystem")
    pr(24, "type", struct.unpack_from("<I", b, 24)[0])
    pr(25, "elen", struct.unpack_from("<I", b, 25)[0])
    pr(26, "alen", struct.unpack_from("<I", b, 26)[0])
    pr(27, "nlen", struct.unpack_from("<I", b, 27)[0])
    pr(28, "block_size", struct.unpack_from("<I", b, 28)[0])
    pr(32, "block_count", struct.unpack_from("<I", b, 32)[0])
    pr(36, "version", hex(struct.unpack_from("<I", b, 36)[0]))
    pr(40, "magic", str(b[40:40 + 8], 'ascii'))


def decode_bootsec_lfs2(b):
    print("Littlefs v2 filesystem")
    pr(8, "magic", str(b[8:8 + 8], "ascii"))
    pr(20, "version", hex(struct.unpack_from("<I", b, 20)[0]))
    pr(24, "block_size", struct.unpack_from("<I", b, 24)[0])
    pr(28, "block_count", struct.unpack_from("<I", b, 28)[0])
    pr(32, "name_max", struct.unpack_from("<I", b, 32)[0])
    pr(36, "file_max", struct.unpack_from("<I", b, 36)[0])
    pr(40, "attr_max", struct.unpack_from("<I", b, 40)[0])


def decode_bootsec(b):
    if b[40:48] == b"littlefs":
        decode_bootsec_lfs1(b)
    elif b[8:16] == b"littlefs":
        decode_bootsec_lfs2(b)
    else:
        decode_bootsec_fat(b)

def main():
    if sys.platform == 'pyboard':
        import pyb
        #sd = pyb.SDCard()
        sd = pyb.Flash(start=0)
        bootsec = bytearray(512)
        sd.readblocks(0, bootsec)
    elif sys.platform in ('esp8266', 'esp32'):
        import esp
        bootsec = bytearray(512)
        esp.flash_read(esp.flash_user_start(), bootsec)
    else:
        with open(sys.argv[1], 'rb') as f:
            bootsec = f.read(512)
    decode_bootsec(bootsec)

main()
