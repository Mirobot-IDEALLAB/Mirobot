import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)
ser.write(b'$H{1}\n')   # homing
time.sleep(1)
ser.close()