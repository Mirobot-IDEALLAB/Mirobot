import serial
import time

ser = serial.Serial("COM6", 115200)
ser.write(b'$H{1}\n')   # homing
time.sleep(1)
ser.close()