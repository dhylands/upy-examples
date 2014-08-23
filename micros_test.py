import pyb

start = pyb.millis()
count = 0
while True:
    pyb.disable_irq()
    m = pyb.millis()
    u = pyb.micros() & 0x7fffffff
    pyb.enable_irq()
    m2 = u // 1000
    if m2 != m:
        if m2 != (m + 1) or (u % 1000) > 100:
            print("msec %d usec %d" % (m, u))
            count += 1
    if (m - start) >= 10000:
        print('%4d err = %d' % (m // 1000, count))
        start = m
        if count > 0:
            break

