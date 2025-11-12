import threading
import queue
import time

class motionQueue:
    def __init__(self, robot):
        self.robot = robot
        self.command_queue = queue.Queue()
        self.running = True

        # 큐를 처리하는 전용 스레드 시작
        self.worker = threading.Thread(target=self._process_commands, daemon=True)
        self.worker.start()

    def _process_commands(self):
        while self.running:
            command, args = self.command_queue.get()  # 큐에서 명령 하나 꺼냄
            try:
                command(*args)  # 명령 실행
            except Exception as e:
                print(f"명령 실행 중 오류 발생: {e}")
            self.command_queue.task_done()  # 실행 완료 표시

    def add_command(self, command, *args):
        """명령을 큐에 추가"""
        self.command_queue.put((command, args))

    def stop(self):
        """스레드 종료"""
        self.running = False
        self.worker.join()