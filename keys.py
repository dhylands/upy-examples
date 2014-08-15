from pyb import USB_VCP

u = USB_VCP()

while True:
    data = u.recv(1)
    ch = data[0]
    if ch < ord(' ') or ch > ord('~'):
        ch = '.'
    print("Rcvd: 0x%x '%c'" % (data[0], ch))

