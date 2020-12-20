# **With DI** ver - 0.9.0

![test](https://blog.kakaocdn.net/dn/bFI2Wu/btqO3z7Sw9s/9xuFEoZQKErjEhw7KBtVA1/img.png)

스터디윗미 방송이나 PC 환경에서 공부하시는 분들을 위한 타이머 프로그램 위드디(with DI)입니다. 가끔씩 유튜브에서 코딩 위드미를 방송하고 있다보니 필수 기능만 구성하고 싶어서 만들게 됐습니다. **개발단계입니다. 오류와 버그는 지속적으로 수정하겠습니다.**  
<br/>
    
 ## **주요 기능**
 1. **OBS 방송 프로그램에 맞게 txt 파일로 타이머가 동작하는 방식**
 2. **현재 날짜, 현재 시간, 공부 시간, 휴식 시간, 식사 시간 등을 타이머로 설정**
 3. **ASMR 링크 음악 재생**
 4. **효과음으로 시작 종료 이벤트** 
 5. ***위젯 생성 [추가 예정]***

## 
![Alt text](https://blog.kakaocdn.net/dn/biOFb7/btqPaVBSEAX/2D2WRZGaI8v0S0YM3zZDV1/img.png)
![Alt text](https://blog.kakaocdn.net/dn/L65F5/btqO3zmw2Ae/pWkuUeCD152Pbzgk6UIXQk/img.png)

## **사용 방법**

 1. **타이머 형식과 추가로 삽일 할 문자열을 지정해줍니다.**
 2. **출력 날짜, 시간은 실제 OBS에서 표현되는 타이머 텍스트입니다.**
 3. **우측 상단의 시작 버튼을 클릭하시면 1초 간격으로 타이머가 업데이트됩니다.**
 4. **이후, 저장 위치의 경로를 복사해주세요.**
 <br/>

![Alt text](https://blog.kakaocdn.net/dn/1pwq0/btqOM9oOOxM/9r5rDdWCbbvsRe6u7RQ3c0/img.png)
![Alt text](https://blog.kakaocdn.net/dn/cDwDVT/btqOP3VYHA7/hDPhkS5cCwAeOUh2wvSJx1/img.png)
 <br/>

 5. **OBS 프로그램에서 텍스트 소스를 추가해줍니다.**
 6. **파일에서 불러들이기를 체크해주시고 복사된 경로의 텍스트 파일을 지정해줍니다.**
 7. **타이머가 작동 중이라면 텍스트 파일이 1초 간격으로 업데이트됩니다.**
 8. **OBS 텍스트 속성에서 폰트와 색상 등을 변경해주시면 됩니다.**


## **다운로드**

소스코드 (python) : https://github.com/DEEPI-LAB/python-study-with-me-timer.git<br/>
배포판 (windows10) : [https://drive.google.com/file](https://drive.google.com/file/d/1J64QTsQikO4AhohP2P5S-aCSBpis-bef/view?usp=sharing)


## **패치노트**

### 2020-12-01 [0.2.0]
### 2020-12-02 [0.2.1]

 - UI 수정
 - 쓰레드 버그 수정
 - 위젯 추가
 - 폴더 트리 단일화

### 2020-12-02 [0.3.0]

 - UI 수정
 - Streaming 위젯 추가
 - 타이머 동작 방식 개선
 - 교시제로 타이머 방식 변경
 - 배포판 용량 축소 1GB -> 40mb

### 2020-12-04 [0.4.0]

 - UI 개선 
 - 음원 재생 오류 수정
 - ASMR 링크 추가
 - 기타 버그 수정

### 2020-12-05 [0.5.0]

 - Config 저장 불러오기 추가
 - UI 개선
 - ASMR 링크 추가
 - 기타 버그 수정
 - 타이머 싱크 개선

### 2020-12-07 [0.6.0]

 - UI 개선
 - 경로 자동 복사기능 추가
 - 기타 버그 수정

### 2020-12-09 [0.8.1]
- UI 개선
- Config 관련 오류 수정
- 경로 자동 복사기능 추가
- 기타 버그 수정
- 음원 압축

### 2020-12-15 [0.8.5]
- UI 개선
- 폰트 변경
- refresh 오류 수정
- 버튼 클릭 이벤트 추가
- 배포판 용량 압축

### 2020-12-20 [0.9.0]
- UI 개선
- 시간형식 버그 수정
- 종료음, 배경음 삭제


## **Contact Us**
blog : https://deep-eye.tistory.com<br/>
mail : deepi.contact.us@gmail.com 