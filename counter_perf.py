import pyb
import micropython

def sk():
  count = 0
  millis = pyb.millis
  print('start')
  kon = millis() + 1000
  while millis() < kon:
    count += 1
  print('normal', count)

@micropython.native
def skn():
  count = 0
  millis = pyb.millis
  print('start')
  kon = millis() + 1000
  while millis() < kon:
    count += 1
  print("native", count)

sk()
skn()

