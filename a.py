import wlkatapython
import serial
import time
import sys

# 이동을 위한 좌표 정의
coordinate_g = [[30, 0, 0, 0, 0, 0],
                [-30, 0, 0, 0, 0, 0],
                [0, 30, 0, 0, 0, 0],
                [0, -30, 0, 0, 0, 0],
                [0, 0, 30, 0, 0, 0],
                [0, 0, -30, 0, 0, 0],
                [0, 0, 0, 30, 0, 0],
                [0, 0, 0, -30, 0, 0],
                [0, 0, 0, 0, 30, 0],
                [0, 0, 0, 0, -30, 0],
                [0, 0, 0, 0, 0, 30],
                [0, 0, 0, 0, 0, -30]]

# --- 설정 ---
COM_PORT = 'COM3'  # 로봇의 실제 COM 포트와 일치하는지 확인하세요.
BAUD_RATE = 115200 # 로봇의 보드레이트와 일치하는지 확인하세요.
ROBOT_ADDRESS = -1 # 기본 주소, 문제가 지속되면 wlkatapython 문서를 확인하세요.

# 시리얼 포트의 추가 설정 (wlkatapython 라이브러리나 로봇 매뉴얼에 따라 필요할 수 있음)
# 일반적으로 8N1 (8 데이터 비트, N 패리티, 1 스톱 비트)이 기본값이지만, 명시적으로 설정해볼 수 있습니다.
SERIAL_BYTESIZE = serial.EIGHTBITS
SERIAL_PARITY = serial.PARITY_NONE
SERIAL_STOPBITS = serial.STOPBITS_ONE
SERIAL_XONXOFF = False # 소프트웨어 흐름 제어 (대부분의 로봇에서 필요 없음)
SERIAL_RTSCTS = False # 하드웨어 흐름 제어 (대부분의 로봇에서 필요 없음)

serial_connection = None
mirobot = None

try:
    # --- 시리얼 연결 설정 ---
    print(f"시리얼 포트 {COM_PORT}를 {BAUD_RATE} 보드레이트로 열려고 시도 중...")
    serial_connection = serial.Serial(
        port=COM_PORT,
        baudrate=BAUD_RATE,
        timeout=1, # 읽기 작업에 타임아웃 추가
        bytesize=SERIAL_BYTESIZE,
        parity=SERIAL_PARITY,
        stopbits=SERIAL_STOPBITS,
        xonxoff=SERIAL_XONXOFF,
        rtscts=SERIAL_RTSCTS
    )
    print("시리얼 포트가 성공적으로 열렸습니다.")

    # --- Mirobot 객체 초기화 ---
    mirobot = wlkatapython.Wlkata_UART()
    print("Mirobot 객체가 생성되었습니다.")

    # --- 로봇 초기화 ---
    print(f"주소 {ROBOT_ADDRESS}로 로봇 초기화 중...")
    # init 메서드는 종종 통신을 설정하기 위한 초기 명령을 보냅니다.
    # -1 상태가 되는 일반적인 이유는 여기서 실패하기 때문입니다.
    mirobot.init(serial_connection, ROBOT_ADDRESS)
    print("로봇 초기화 명령이 전송되었습니다.")
    time.sleep(1) # 초기화 후 로봇이 응답할 시간을 줍니다.

    # --- 초기 로봇 상태 확인 ---
    # -1 (오류) 또는 'Alarm' 상태가 아닐 때까지 지속적으로 상태를 확인하는 루프
    # 이는 통신이 전혀 설정되었는지 진단하는 데 도움이 됩니다.
    current_state = mirobot.getState()
    print(f"초기 로봇 상태: {current_state}")

    # getState()가 -1을 반환하면 통신 오류 또는 로봇이 준비되지 않았음을 의미합니다.
    # 'Alarm' 상태 또는 유사한 알려진 상태일 때만 호밍을 시도해야 합니다.
    # -1인 경우 로봇을 다시 시작하거나 물리적 연결을 확인해야 할 수 있습니다.
    if current_state == -1:
        print("경고: 로봇 상태가 -1입니다. 이는 일반적으로 통신 오류 또는 로봇이 준비되지 않았음을 나타냅니다.")
        print("로봇 전원이 켜져 있고, 올바르게 연결되었으며, COM 포트가 정확한지 확인하세요.")
        print("다시 초기화를 시도하고 상태를 다시 확인 중...")
        time.sleep(2) # 재시도 전에 잠시 기다립니다.
        mirobot.init(serial_connection, ROBOT_ADDRESS) # 다시 초기화 시도
        time.sleep(1)
        current_state = mirobot.getState()
        print(f"재초기화 시도 후 로봇 상태: {current_state}")
        if current_state == -1:
            raise Exception("로봇과의 통신 설정에 실패했습니다. 상태가 -1로 유지됩니다.")

    # --- 호밍 프로세스 ---
    # 호밍은 로봇이 'Alarm' 또는 유휴 상태가 아니고 통신이 확인된 경우(상태가 -1이 아님)에만 시도해야 합니다.
    if current_state == "Alarm" or current_state != "Idle":
        print("로봇이 유휴 상태가 아니거나 알람 상태입니다. 호밍 프로세스를 시작합니다...")
        print("호밍 명령을 전송하기 전에 잠시 대기합니다...")
        time.sleep(1) # 호밍 명령 전 추가 대기 (로봇이 명령을 받을 준비가 되도록)
        
        print("호밍 명령을 전송합니다...")
        mirobot.homing()
        print("호밍 명령이 전송되었습니다. 로봇이 유휴 상태가 되기를 기다리는 중...")

        # 호밍이 완료되고 로봇이 유휴 상태가 될 때까지 기다립니다.
        start_time = time.time()
        HOMING_TIMEOUT = 90 # 초 (이전 60초에서 증가, 충분한 시간 부여)
        while current_state != "Idle":
            current_state = mirobot.getState()
            print(f"로봇이 호밍을 마칠 때까지 기다리는 중... 현재 상태: {current_state} (경과 시간: {time.time() - start_time:.1f}초)")
            time.sleep(1) # 다시 확인하기 전에 잠시 기다립니다.

            if time.time() - start_time > HOMING_TIMEOUT:
                print(f"오류: 호밍이 {HOMING_TIMEOUT}초 후에 시간 초과되었습니다. 로봇이 유휴 상태가 되지 않았습니다.")
                print("로봇의 전원, 물리적 연결, 또는 로봇 자체의 오류 표시등을 확인하세요.")
                raise Exception("호밍 프로세스 시간 초과.")
            
            # 호밍 대기 중에 상태가 -1을 반환하면 통신 손실을 나타냅니다.
            if current_state == -1:
                print("오류: 호밍 프로세스 중 통신이 끊겼습니다 (상태가 -1을 반환했습니다).")
                print("시리얼 포트 연결 또는 로봇 전원을 확인하세요.")
                raise Exception("호밍 중 통신 손실.")

        print("호밍 완료, 로봇이 유휴 상태입니다.")
    else:
        print("로봇이 이미 유휴 상태이거나 준비된 상태입니다. 호밍을 건너뜁니다.")

    # --- 로봇 팔을 좌표를 통해 이동 ---
    for i, coords in enumerate(coordinate_g):
        print(f"\n위치 {i + 1}로 이동 중...")

        # 다음 명령을 보내기 전에 로봇이 유휴 상태가 될 때까지 기다립니다.
        # 이 루프는 로봇이 바쁠 때 명령을 보내는 것을 방지하는 데 중요합니다.
        # 특정 복구 메커니즘이 아닌 한 이 루프 내에서 homing()을 호출하지 마십시오.
        start_time_move = time.time()
        MOVE_IDLE_TIMEOUT = 15 # 초
        while mirobot.getState() != "Idle":
            state_during_move_wait = mirobot.getState()
            print(f"다음 이동 명령 전에 로봇이 유휴 상태가 되기를 기다리는 중... 현재 상태: {state_during_move_wait} (경과 시간: {time.time() - start_time_move:.1f}초)")
            time.sleep(0.5) # 응답성을 위해 짧은 대기

            if time.time() - start_time_move > MOVE_IDLE_TIMEOUT:
                print(f"오류: {MOVE_IDLE_TIMEOUT}초 후 다음 이동 명령 전에 로봇이 유휴 상태가 되지 않았습니다.")
                raise Exception("로봇이 멈춰서 다음 이동을 위해 유휴 상태가 되지 않습니다.")
            
            if state_during_move_wait == -1:
                print("오류: 이동 대기 중 통신이 끊겼습니다 (상태가 -1을 반환했습니다).")
                raise Exception("이동 대기 중 통신 손실.")


        # 이동 명령 전송
        print(f"위치 {i + 1}에 대한 각도 명령 전송: {coords}")
        # 6개의 모든 각도가 올바르게 전달되는지 확인하세요.
        mirobot.writeangle(0, coords[0], coords[1], coords[2], coords[3], coords[4], coords[5])
        time.sleep(2) # 로봇이 움직임을 시작하고 안정화될 시간을 줍니다.

    # --- 로봇 팔을 초기 위치로 복귀 ---
    print("\n로봇을 초기 위치(제로)로 복귀 중...")
    mirobot.zero()
    print("제로 명령 전송. 로봇이 유휴 상태가 되기를 기다리는 중...")

    # 제로 복귀가 완료될 때까지 기다립니다.
    start_time_zero = time.time()
    ZERO_TIMEOUT = 15 # 초
    while mirobot.getState() != "Idle":
        state_during_zero_wait = mirobot.getState()
        print(f"로봇이 제로 복귀를 마칠 때까지 기다리는 중... 현재 상태: {state_during_zero_wait} (경과 시간: {time.time() - start_time_zero:.1f}초)")
        time.sleep(1)

        if time.time() - start_time_zero > ZERO_TIMEOUT:
            print(f"오류: 제로 복귀가 {ZERO_TIMEOUT}초 후에 시간 초과되었습니다. 로봇이 유휴 상태가 되지 않았습니다.")
            raise Exception("제로 복귀 프로세스 시간 초과.")
        
        if state_during_zero_wait == -1:
            print("오류: 제로 복귀 대기 중 통신이 끊겼습니다 (상태가 -1을 반환했습니다).")
            raise Exception("제로 복귀 대기 중 통신 손실.")

    print("로봇이 초기 위치로 복귀했으며 유휴 상태입니다.")

except serial.SerialException as e:
    print(f"시리얼 오류: 시리얼 포트 {COM_PORT}를 열 수 없습니다. 포트가 올바르고 다른 애플리케이션에서 사용 중이 아닌지 확인하세요.", file=sys.stderr)
    print(f"세부 정보: {e}", file=sys.stderr)
except Exception as e:
    print(f"로봇 제어 오류: 예상치 못한 오류가 발생했습니다: {e}", file=sys.stderr)
    print("로봇 전원, 물리적 연결을 확인하고 wlkatapython 라이브러리가 올바르게 설치되고 호환되는지 확인하세요.", file=sys.stderr)
finally:
    # --- 시리얼 포트 닫기 ---
    if serial_connection and serial_connection.is_open:
        print("\n시리얼 포트를 닫습니다.")
        serial_connection.close()
        print("시리얼 포트가 닫혔습니다.")
    else:
        print("\n시리얼 포트가 열려 있지 않거나 이미 닫혔습니다.")

