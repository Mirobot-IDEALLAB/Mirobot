#%%
# from MirobotAPI import MirobotAPI as Motion
from motion2 import Motion
from dotenv import load_dotenv
import serial
import time
import os
#%%
load_dotenv()

# 시리얼 통신 설정
COM_PORT = os.getenv('COM_PORT')
BAUD_RATE = os.getenv('BAUD_RATE')

robot = Motion(serial_port=COM_PORT, baud_rate=BAUD_RATE)
print(robot.get_state())

#%%
# robot.homing()
# time.sleep(5)  # 홈 위치로 이동할 시간을 줌
print(robot.get_state())
for i in range(1, 7): 
    print(robot.getCoordinate(i))

coordinates = [198.6 , 0 , 90.7 , 0 , 0 , 0]
robot.writeCoordinate(coordinates, motion=0, position=0)
print(robot.get_state())
#%%

robot.zero()


