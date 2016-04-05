import pyb
import select

# assume UART4 Tx (X1) connected to UART6 Rx (Y2)

u4 = pyb.UART(4, 9600)
u6 = pyb.UART(6, 9600)

u4.write('123')

poll = select.poll()
poll.register(u6, select.POLLIN)
while True:
    events = poll.poll()
    print('events =', events)
    for file in events:
        # file is a tuple
        if file[0] == u6:
            ch = u6.read(1)
            print('Got ', ch)


