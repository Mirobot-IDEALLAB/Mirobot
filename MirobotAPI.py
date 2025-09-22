# mirobot_api.py (wlkatapython 기반)

from motion import Motion  # 네가 만든 Motion 클래스를 불러온다고 가정
import time

class MirobotAPI:
    def __init__(self, port="COM5", baud_rate=115200):
        # 실제 환경에 맞는 포트/보레이트를 넣어라
        self.arm = Motion(serial_port=port, baud_rate=baud_rate)

    # Homing
    def home(self):
        self.arm.homing()

    def zero(self):
        self.arm.zero()

    # Cartesian 이동 (x,y,z,a,b,c = 6자유도)
    def move_xyzrpy(self, x, y, z, a=0, b=0, c=0, motion=1, position=0):
        """
        motion: 0-fast, 1-linear, 2-door type
        position: 0-absolute, 1-relative
        """
        # 안전 체크 필요시 safety로 감쌀 것
        self.arm.mirobot.writecoordinate(motion, position, x, y, z, a, b, c)
        time.sleep(1)

    # 그리퍼
    def grip_open(self):
        self.arm.mirobot.gripper(1)  # 1=open
        time.sleep(1)

    def grip_close(self):
        self.arm.mirobot.gripper(2)  # 2=close
        time.sleep(1)

    # 펌프 (선택)
    def pump_on(self):
        self.arm.mirobot.pump(1)  # suck
        time.sleep(1)

    def pump_off(self):
        self.arm.mirobot.pump(0)  # off
        time.sleep(1)

    # 메시지 출력
    def say(self, msg: str):
        print(f"[Robot] {msg}")
