from motion2 import Motion
from dotenv import load_dotenv
import serial
import time
import os

load_dotenv()

# 시리얼 통신 설정
# COM_PORT = os.getenv('COM_PORT')
# BAUD_RATE = os.getenv('BAUD_RATE')

robot = Motion(serial_port="/dev/ttyUSB0", baud_rate=115200)

# robot.homing()
# time.sleep(5)  # 홈 위치로 이동할 시간을 줌
time.sleep(10)
for i in range(1, 7): 
    print(robot.getCoordinate(i))

# coordinates = [60.0, 0.0, 90, 0.0, 0.0, 0.0]
# robot.writeCoordinate(coordinates, motion=0, position=0)

time.sleep(2)
robot.zero()