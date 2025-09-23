# mirobot_api.py (wlkatapython 기반)

import wlkatapython
import serial
import time

class MirobotAPI:
    def __init__(self, port="COM5", baud_rate=115200):
        self.serial_port = port
        self.baud_rate = baud_rate
        self.mirobot = wlkatapython.Mirobot_UART()
        self.serial_connection = serial.Serial(self.serial_port, self.baud_rate)
        self.mirobot.init(self.serial_connection, -1)
        self.mirobot.homing()


    # Homing
    def home(self):
        self.mirobot.homing()
        time.sleep(1)

    def zero(self):
        self.mirobot.zero()
        time.sleep(1)

    def cancel(self):
        """Cancel the current operation."""
        self.mirobot.cancellation()
        time.sleep(1)
    
    # Cartesian 이동 (x,y,z,a,b,c = 6자유도)
    def move_xyzrpy(self, x, y, z, a=0, b=0, c=0, motion=1, position=0):
        """
        motion: 0-fast, 1-linear, 2-door type
        position: 0-absolute, 1-relative
        """
        # 안전 체크 필요시 safety로 감쌀 것
        self.mirobot.writecoordinate(motion, position, x, y, z, a, b, c)
        time.sleep(1)

    # 그리퍼
    def grip_open(self):
        self.mirobot.gripper(1)  # 1=open
        time.sleep(1)

    def grip_close(self):
        self.mirobot.gripper(2)  # 2=close
        time.sleep(1)

    # 펌프 (선택)
    def pump_on(self):
        self.mirobot.pump(1)  # suck
        time.sleep(1)

    def pump_off(self):
        self.mirobot.pump(0)  # off
        time.sleep(1)

    # 메시지 출력
    def say(self, msg: str):
        print(f"[Robot] {msg}")
