import wlkatapython
import serial
import time

# 아래 코드는 prompt에서 사용하기 위해 작성된 코드임
# wlkatapython 라이브러리를 참고하여 직접 작성한 Motion 클래스
# wlkatapython에서 제공하는 동작 뿐만 아니라, 다른 동작도 추가할 수 있음

class Motion:
    def __init__(self, serial_port, baud_rate):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.mirobot = wlkatapython.Mirobot_UART()
        self.serial_connection = serial.Serial(self.serial_port, self.baud_rate)
        self.mirobot.init(self.serial_connection, -1)
        self.mirobot.homing()


    def homing(self):
        """Return the robot arm to its zero position and idle state."""
        self.mirobot.homing()
        time.sleep(1)


    def zero(self):
        """Return the robot arm to its zero position."""
        self.mirobot.zero()
        time.sleep(1)

    def cancellation(self):
        """Cancel the current operation."""
        self.mirobot.cancellation()
        time.sleep(1)
    

    def writeCoordinate(self, coordinates, motion=1, position=1):
        """control robotic arm in Cartesian coordinate."""
        print(f"Moving to coordinates: {coordinates} with motion={motion}, position={position}")
        self.mirobot.writecoordinate(motion, position, *coordinates)
        time.sleep(1)


    def writeAngle(self):
        """Control robotic arm in angle mode"""
        position = int(input("0 - absolute, 1 - relative:"))
        if position not in [0, 1]:
            print("잘못된 입력입니다. 0 또는 1을 입력하세요.")
            return
        
        angles = list(map(float, input("x y z a b c 각도를 입력하세요 (공백으로 구분): ").strip().split()))
        if len(angles) != 6:
            print("잘못된 각도 입력입니다. a, b, c, d, e, f 각도를 입력하세요.")
            return
        
        self.mirobot.writeangle(position, *angles)
        time.sleep(1)


    def close(self):
        """Close the serial connection."""
        self.mirobot.homing()   # return to zero position
        time.sleep(1)
        self.serial_connection.close()