from motion2 import Motion
from dotenv import load_dotenv
import serial
import time
import os

load_dotenv()

# 시리얼 통신 설정
COM_PORT = os.getenv('COM_PORT')
BAUD_RATE = os.getenv('BAUD_RATE')

robot = Motion(serial_port=COM_PORT, baud_rate=BAUD_RATE)

robot.homing()
time.sleep(5)  # 홈 위치로 이동할 시간을 줌

coordinates = [60.0, 0.0, 0.0, 0.0, 0.0, 0.0]
robot.writeCoordinate(coordinates, motion=1, position=1)

time.sleep(2)
robot.zero()