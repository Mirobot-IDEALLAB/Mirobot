import wlkatapython
import serial
import time

# 아래 코드는 prompt에서 사용하기 위해 작성된 코드임
# wlkatapython 라이브러리를 참고하여 직접 작성한 Motion 클래스
# wlkatapython에서 제공하는 동작 뿐만 아니라, 다른 동작도 추가할 수 있음

class Motion:
    def __init__(self, serial_port="COM7", baud_rate=115200):
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
        self.mirobot.homing()
        time.sleep(1)

    def runFile(self, file_path):
        """Run a file on the robot arm."""
        self.mirobot.runFile(file_path, num=False)  # num -> loop
        time.sleep(1)



    def close(self):
        """Close the serial connection."""
        self.mirobot.homing()   # return to zero position
        time.sleep(1)
        self.serial_connection.close()