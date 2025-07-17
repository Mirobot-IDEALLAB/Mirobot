from motion import Motion
import time

robot = Motion(serial_port="/dev/ttyUSB0", baud_rate=115200)

command_map = {
    "help": lambda: print("사용 가능한 명령어: " + ", ".join(command_map.keys())),
    "homing": robot.homing,
    "zero": robot.zero,
    "runfile": robot.runFile,
    "cancellation": robot.cancellation,
    "pump": robot.pump,
    "gripper": robot.gripper,
    "writecoordinate": robot.writeCoordinate,
    "writeangle": robot.writeAngle,
    "close": robot.close
}

while True:
    print(f"현재 로봇 상태: {robot.mirobot.getState()}")
    cmd = input("명령을 입력하세요 (명령어를 보려면 help를 입력하세요): ").strip().lower()
    if cmd in command_map:
        command_map[cmd]()
        print(f"{cmd} 명령이 실행되었습니다.")
        if cmd == "close":
            print("프로그램을 종료합니다.")
            break
        time.sleep(1)

    else:
        print("알 수 없는 명령입니다. 다시 시도하세요.")