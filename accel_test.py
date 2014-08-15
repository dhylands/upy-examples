import pyb
acc = pyb.Accel()
while True:
    print(acc.x(), acc.y(), acc.z())
    pyb.delay(1000)
