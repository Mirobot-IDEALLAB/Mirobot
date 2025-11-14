# Mirobot
### Connecting Mirobot with Python (without Wlkata studio)

- 코드 바로 실행   
주의 사항 : 로봇은 한 번에 한 동작만 가능, 동시 입력 시 오류 가능성 있음 (보통 먼저 입력된 명령어만 처리)   
- 해결방안   
1. time.sleep() 활용
2. 로봇의 상태를 실시간으로 받아 동작할 수 있을 때까지 대기 (o)


+ vla

일반적으로 로봇팔 제어
비전 -- 자연어 -- 제어
이 과정에서 llm을 사용함
-> 현재 하는 작업은 자연어를 정책 제어 코드로 변환하는 작업이므로, 큰 용량의 모델이 필요 없음
방향성 정해야 할듯

### pip list
|Package|Version|
|-----------|-----|
|pip|25.1.1|
|pyserial|3.5|
|wlkatapython|0.1.0|