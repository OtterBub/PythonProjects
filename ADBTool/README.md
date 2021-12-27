ADBTool for MultiDevices and More Easy
TEST ENC Park SungKyoung 
20211013 Update

파일 요약
[ ADBCapturePacket.exe - 패킷 캡쳐 명령어 실행 ]
[ ADBCapturePacketOutput.exe - 패킷 캡쳐 파일 추출 실행 ]
[ ADBLogcatOutput.exe - 실시간 로그파일 추출 실행 ]
[ ADBAutoInstallAPK.exe - APK 설치기 ]

------------ 사용법 -----------------

원하는 기능의 .exe 실행
USB 포트에 원하는 만큼 기기 연결

또는

USB 포트에 원하는 만큼 기기 연결
원하는 기능의 .exe 실행

* 명령어 다시 실행하기
- 단말 재연결 하거나
- 프로그램 재실행

------------ 화면 설명 -----------------

[작동화면.png 참고]

Status 
IDLE: 명령어 수행 전 (또는 에러 나서 실행 안됨)
COMPLETE: 명령어 수행 완료

CAPTURING PACKET: 패킷 캡쳐중
SENDING DATA: 데이터 내보내는중
RECORDING LOG: 로그 기록중

기기 상태 위에 CONNECT -> 현재 연결된 기기
표시 안되었을 경우 연결 안된 기기

------------ 내부 작동 원리 -----------------

기본은 adb 명령어 실행과 동일
멀티쓰레드를 이용하여 명령어를 동시에 수행

------------ 각 파일 설명 -----------------

[ ADBCapturePacket.exe - 패킷 캡쳐 명령어 실행 ]
- adb shell tcpdump -i any -p -s 0 -w /sdcard/PhoneNumber_모델명.pcap
- 폰 내부 /sdcard/ 폴더에 PhoneNumber_모델명.pcap으로 기록
- IDLE 상태이거나 명령어 실행 않고 COMPLETE 상태가 된다면 해당 폰 명령어 실행 불가
- 연결 해제할 필요는 없음

[ ADBCapturePacketOutput.exe - 패킷 캡쳐 파일 추출 실행 ]
- adb pull /sdcard/PhoneNumber_모델명.pcap .
- .exe 실행한 폴더에 PhoneNumber_모델명.pcap 파일 추출

[ ADBLogcatOutput.exe - 실시간 로그파일 추출 실행 ]
- adb logcat -v threadtime > ./PhoneNumber_모델명_현재날짜시간(시분초).log
- .exe 실행한 폴더에 PhoneNumber_모델명.log 파일 추출

[ ADBAutoInstallAPK.exe - APK 설치기 ]
- adb install -r -d "파일명"
- 그냥 실행시 apk 선택창 노출
- 끌어다 놓아도 실행 가능
- apk 기본 실행 파일로 해당 실행파일 지정하면 매우 편함

[ ADBUninstallMeetUs.exe - MeetUs Android App 삭제기 ]

[ Appium.exe - Run Appium Test For MeetUs ]

[ Pyinstaller(py to exe).exe ]
- pyinstaller 폴더내 py 모두 exe로 바꿈 자동 실행
- pyinstaller 필요

[ Pycleaner.exe ]
- 폴더내 특정 확장자 정리 코드
- json, pcap, log

sourcecode 폴더
- 파이썬 소스코드



- Changed Log -
211227
- shell getprop 명령어 결과값에 한글 출력시 에러 나는 현상 수정
-- subprocess.check_output(encoding='UTF8') 로 수정함

211013
- shell getprop 명령어 실패시 프로그램 안꺼지게 임시조치
-- 결과값에 한글이 포함될 경우 'UnicodeDecodeError' 노출됨
- CONNECT/DISCONNECT, ERROR 텍스트 색상 변경
- ADBCommand Module 버전 값 추가
- 전체 스크립트에 ADBCommand Module 버전 프린트 행 추가

210226
- 에러 상태일때 커맨드 자동 반복 안되게끔 수정
- 에러상태 제대로 반영되도록 수정

210207
- 쓰레드 예외 처리중 키보드 인터럽트 예외 추가

210120
- 디바이스 정보 추가 (Build Tags / Type)
- custom 모듈 수정
-- subprocess로 다시 교체

210107
- custom 모듈 수정
- adb devices 오류 예외 처리 추가
- logcat 용량 기록 추가

201230
- 공통 소스 모듈 custom으로 추출
- subprocess에서 os.system으로 명령어 실행
- PhoneNumber 서칭 스레드 변경 (속도 개선)
- ADBLogcatOutput
-- 모델명_현재날짜시간(시분초).log 로 로그 겹치지 않게 추출
- 사용법, 작동화면 설명 추가

201224
- ADBCapturePacket 추가
-- AutoInstallAPK 변형
- Issue
-- subprocess로 실행 안되는 명령어 존재중...
-- os.system 으로 대체 ( ADBLogcatOutput )