import serial
import time
import numpy as np

teensy = serial.Serial(port='/dev/cu.usbmodem157539901',  baudrate=115200, timeout=.1)


def readowrito():
    teensy.write(bytearray([255]))
    data = np.frombuffer(teensy.read(36), dtype=np.uint8)
    return  data


while True:
    num = input("Enter a number: ")
    before = time.perf_counter()
    value  = readowrito()
    after  = time.perf_counter()
    print(after-before, value)
