# Mirobot
### Connecting Mirobot with Python (without Wlkata studio)

- 코드 바로 실행   
문제점 : 보안, 코드 오류 시 원인 파악이 어려움
대안 : 언어 모델이 코드 전체 출력이 아닌, 명령 리스트만 반환하도록 하기 (json형태)

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