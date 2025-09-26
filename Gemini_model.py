from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

API_KEY = os.getenv('Gemini_API_KEY')

client = genai.Client(api_key=API_KEY)

# 시리얼 통신 설정
COM_PORT = os.getenv('COM_PORT')
BAUD_RATE = os.getenv('BAUD_RATE')

# system_prompt 설정 (코드만 출력하도록 지시)
system_prompt = """
너는 Python 로봇 제어 코드 변환기이다.  
사용자가 자연어로 명령하면, 이를 MirobotAPI 클래스의 메서드를 사용한 실행 가능한 Python 코드로 변환한다.  
항상 순수 코드만 출력해야 하며, 불필요한 설명은 쓰지 않는다.  
"""

# context 설정 
context = """
MirobotAPI 클래스의 주요 메서드:

- home(): 로봇을 초기 위치로 이동
- zero(): 현재 위치를 원점으로 설정
- cancel(): 현재 동작을 취소
- move_xyzrpy(x, y, z, a=0, b=0, c=0, motion=1, position=0)
    - x, y, z: 로봇 팔 위치
    - a, b, c: 회전 (roll, pitch, yaw)
    - motion: 0=빠른 이동, 1=직선 이동, 2=문 여는 형식 이동
    - position: 0=절대 좌표, 1=상대 좌표

좌표계 규칙:
- "오른쪽" → x축 양수 이동
- "왼쪽" → x축 음수 이동
- "앞으로" → y축 양수 이동
- "뒤로" → y축 음수 이동
- "위로" → z축 양수 이동
- "아래로" → z축 음수 이동
"""

user_prompt = '로봇팔을 오른쪽으로 10만큼 움직여'

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[system_prompt, context, user_prompt],
    config={"temperature": 0.2} # 응답 일관성 유지 위해 낮은 온도 설정
)
print(response.text)