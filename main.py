from Gemini_model import ready_model 
from MirobotAPI import MirobotAPI
from dotenv import load_dotenv
import serial
import time
import os

load_dotenv()

# 시리얼 통신 설정
COM_PORT = os.getenv('COM_PORT')
BAUD_RATE = os.getenv('BAUD_RATE')

robot = MirobotAPI(port=COM_PORT, baud_rate=BAUD_RATE)

robot.home()
time.sleep(2)  # 홈 위치로 이동할 시간을 줌

output = ready_model()

print(f"Generated Code:\n{output}")
exec(output)