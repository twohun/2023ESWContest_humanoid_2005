


'******** 2족 보행로봇 초기 영점 프로그램 ********

DIM I AS BYTE
DIM J AS BYTE
DIM MODE AS BYTE
DIM A AS BYTE
DIM A_old AS BYTE
DIM B AS BYTE
DIM C AS BYTE
DIM 보행속도 AS BYTE
DIM 좌우속도 AS BYTE
DIM 좌우속도2 AS BYTE
DIM 보행순서 AS BYTE
DIM 현재전압 AS BYTE
DIM 반전체크 AS BYTE
DIM 모터ONOFF AS BYTE
DIM 자이로ONOFF AS BYTE
DIM 기울기앞뒤 AS INTEGER
DIM 기울기좌우 AS INTEGER

DIM 곡선방향 AS BYTE

DIM 넘어진확인 AS BYTE
DIM 기울기확인횟수 AS BYTE
DIM 보행횟수 AS BYTE
DIM 보행COUNT AS BYTE

DIM 적외선거리값  AS BYTE

DIM S11  AS BYTE
DIM S16  AS BYTE
'************************************************
DIM NO_0 AS BYTE
DIM NO_1 AS BYTE
DIM NO_2 AS BYTE
DIM NO_3 AS BYTE
DIM NO_4 AS BYTE

DIM NUM AS BYTE

DIM BUTTON_NO AS INTEGER
DIM SOUND_BUSY AS BYTE
DIM TEMP_INTEGER AS INTEGER

'**** 기울기센서포트 설정 ****
CONST 앞뒤기울기AD포트 = 0
CONST 좌우기울기AD포트 = 1
CONST 기울기확인시간 = 20  'ms

CONST 적외선AD포트  = 4


CONST min = 61	'뒤로넘어졌을때
CONST max = 107	'앞으로넘어졌을때
CONST COUNT_MAX = 3


CONST 머리이동속도 = 10
'************************************************



PTP SETON 				'단위그룹별 점대점동작 설정
PTP ALLON				'전체모터 점대점 동작 설정

DIR G6A,1,0,0,1,0,0		'모터0~5번
DIR G6D,0,1,1,0,1,1		'모터18~23번
DIR G6B,1,1,1,1,1,1		'모터6~11번
DIR G6C,0,0,0,1,1,0		'모터12~17번

'************************************************

OUT 52,1

,0	'머리 LED 켜기
'***** 초기선언 '************************************************

보행순서 = 0
반전체크 = 0
기울기확인횟수 = 0
보행횟수 = 1
모터ONOFF = 0

'****초기위치 피드백*****************************


'TEMPO 230
'MUSIC "cdefg"
'TEMPO 200
'MUSIC "abc"



SPEED 5
GOSUB MOTOR_ON

S11 = MOTORIN(11)
S16 = MOTORIN(16)

SERVO 11, 100
SERVO 16, S16

SERVO 16, 100


GOSUB 전원초기자세
GOSUB 기본자세


GOSUB 자이로INIT
GOSUB 자이로MID
GOSUB 자이로ON



PRINT "VOLUME 200 !"
'PRINT "SOUND 12 !" '안녕하세요

GOSUB All_motor_mode3





GOTO MAIN	'시리얼 수신 루틴으로 가기

'************************************************

'*********************************************
' Infrared_Distance = 60 ' About 20cm
' Infrared_Distance = 50 ' About 25cm
' Infrared_Distance = 30 ' About 45cm
' Infrared_Distance = 20 ' About 65cm
' Infrared_Distance = 10 ' About 95cm
'*********************************************
'************************************************
시작음:
    TEMPO 220
    MUSIC "O23EAB7EA>3#C"
    RETURN
    '************************************************
종료음:
    TEMPO 220
    MUSIC "O38GD<BGD<BG"
    RETURN
    '************************************************
에러음:
    TEMPO 250
    MUSIC "FFF"
    RETURN
    '************************************************
    '************************************************
MOTOR_ON: '전포트서보모터사용설정

    GOSUB MOTOR_GET

    MOTOR G6B
    DELAY 50
    MOTOR G6C
    DELAY 50
    MOTOR G6A
    DELAY 50
    MOTOR G6D

    모터ONOFF = 0
    'GOSUB 시작음			
    RETURN

    '************************************************
    '전포트서보모터사용설정
MOTOR_OFF:

    MOTOROFF G6B
    MOTOROFF G6C
    MOTOROFF G6A
    MOTOROFF G6D
    모터ONOFF = 1	
    GOSUB MOTOR_GET	
    GOSUB 종료음	
    RETURN
    '************************************************
    '위치값피드백
MOTOR_GET:
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,1,1,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN

    '************************************************
    '위치값피드백
MOTOR_SET:
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,1,1,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN

    '************************************************
All_motor_Reset:

    MOTORMODE G6A,1,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1,1
    MOTORMODE G6B,1,1,1,,,1
    MOTORMODE G6C,1,1,1,1,1

    RETURN
    '************************************************
All_motor_mode2:

    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    MOTORMODE G6B,2,2,2,,,2
    MOTORMODE G6C,2,2,2,2,2

    RETURN
    '************************************************
All_motor_mode3:

    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    MOTORMODE G6B,3,3,3,,,3
    MOTORMODE G6C,3,3,3,3,3

    RETURN
    '************************************************
Leg_motor_mode1:
    MOTORMODE G6A,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1
    RETURN
    '************************************************
Leg_motor_mode2:
    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    RETURN

    '************************************************
Leg_motor_mode3:
    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    RETURN
    '************************************************
Leg_motor_mode4:
    MOTORMODE G6A,3,2,2,1,3
    MOTORMODE G6D,3,2,2,1,3
    RETURN
    '************************************************
Leg_motor_mode5:
    MOTORMODE G6A,3,2,2,1,2
    MOTORMODE G6D,3,2,2,1,2
    RETURN
    '************************************************
Arm_motor_mode1:
    MOTORMODE G6B,1,1,1,,,1
    MOTORMODE G6C,1,1,1,1,1
    RETURN
    '************************************************
Arm_motor_mode2:
    MOTORMODE G6B,2,2,2,,,2
    MOTORMODE G6C,2,2,2,2,2
    RETURN

    '************************************************
Arm_motor_mode3:
    MOTORMODE G6B,3,3,3,,,3
    MOTORMODE G6C,3,3,3,3,3
    RETURN
    '************************************************

전원초기자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  35,  90, 190
    WAIT
    mode = 0
    RETURN
    '************************************************
안정화자세:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  35,  90, 190
    WAIT
    mode = 0

    RETURN
    '******************************************	


    '************************************************
기본자세:


    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 0

    RETURN
    '******************************************	
기본자세2:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT

    mode = 0
    RETURN
    '******************************************	
차렷자세:
    MOVE G6A,100, 56, 182, 76, 100, 100
    MOVE G6D,100, 56, 182, 76, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 2
    RETURN
    '******************************************
앉은자세:
    GOSUB 자이로OFF
    MOVE G6A,100, 145,  28, 145, 100, 100
    MOVE G6D,100, 145,  28, 145, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 1

    RETURN
    '******************************************
    '***********************************************
    '***********************************************
    '**** 자이로감도 설정 ****
자이로INIT:

    GYRODIR G6A, 0, 0, 1, 0,0
    GYRODIR G6D, 1, 0, 1, 0,0

    GYROSENSE G6A,200,150,30,150,0
    GYROSENSE G6D,200,150,30,150,0

    RETURN
    '***********************************************
    '**** 자이로감도 설정 ****
자이로MAX:

    GYROSENSE G6A,250,180,30,180,0
    GYROSENSE G6D,250,180,30,180,0

    RETURN
    '***********************************************
자이로MID:

    GYROSENSE G6A,200,150,30,150,0
    GYROSENSE G6D,200,150,30,150,0

    RETURN
    '***********************************************
자이로MIN:

    GYROSENSE G6A,200,100,30,100,0
    GYROSENSE G6D,200,100,30,100,0
    RETURN
    '***********************************************
자이로ON:

    GYROSET G6A, 4, 3, 3, 3, 0
    GYROSET G6D, 4, 3, 3, 3, 0

    자이로ONOFF = 1

    RETURN
    '***********************************************
자이로OFF:

    GYROSET G6A, 0, 0, 0, 0, 0
    GYROSET G6D, 0, 0, 0, 0, 0


    자이로ONOFF = 0
    RETURN

    '************************************************

    '******************************************
    '**********************************************
    '**********************************************
RX_EXIT:

    ERX 4800, A, MAIN

    GOTO RX_EXIT
    '**********************************************
GOSUB_RX_EXIT:

    ERX 4800, A, GOSUB_RX_EXIT2

    GOTO GOSUB_RX_EXIT

GOSUB_RX_EXIT2:
    RETURN
    '**********************************************
    '**********************************************

연속전진_골프:
    보행COUNT = 0
    보행속도 = 13
    좌우속도 = 4
    넘어진확인 = 0

    GOSUB Leg_motor_mode3

    IF 보행순서 = 0 THEN
        보행순서 = 1

        SPEED 4

        MOVE G6A, 88,  74, 144,  95, 110
        MOVE G6D,108,  76, 146,  93,  96
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        SPEED 10'

        MOVE G6A, 90, 90, 120, 105, 110,100
        MOVE G6D,110,  76, 147,  93,  96,100
        MOVE G6B,90
        MOVE G6C,110
        WAIT


        GOTO 연속전진_골프_1	
    ELSE
        보행순서 = 0

        SPEED 4

        MOVE G6D,  88,  74, 144,  95, 110
        MOVE G6A, 108,  76, 146,  93,  96
        MOVE G6C, 100
        MOVE G6B, 100
        WAIT

        SPEED 10

        MOVE G6D, 90, 90, 120, 105, 110,100
        MOVE G6A,110,  76, 147,  93,  96,100
        MOVE G6C,90
        MOVE G6B,110
        WAIT


        GOTO 연속전진_골프_2	

    ENDIF


    '*******************************


연속전진_골프_1:

    ETX 4800,11 '진행코드를 보냄
    SPEED 보행속도

    MOVE G6A, 86,  56, 145, 115, 110
    MOVE G6D,108,  76, 147,  93,  96
    WAIT


    SPEED 좌우속도
    GOSUB Leg_motor_mode3

    MOVE G6A,110,  76, 147, 93,  96
    MOVE G6D,86, 100, 145,  69, 110
    WAIT


    SPEED 보행속도

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO MAIN
    ENDIF

    ERX 4800,A, 연속전진_골프_2
    IF A = 11 THEN
        GOTO 연속전진_골프_2
    ELSE
        ' GOSUB Leg_motor_mode3

        MOVE G6A,112,  76, 146,  93, 96,100
        MOVE G6D,90, 100, 100, 115, 110,100
        MOVE G6B,110
        MOVE G6C,90
        WAIT
        HIGHSPEED SETOFF

        SPEED 8
        MOVE G6A, 106,  76, 146,  93,  96,100		
        MOVE G6D,  88,  71, 152,  91, 106,100
        MOVE G6B, 100
        MOVE G6C, 100
        WAIT	

        SPEED 2
        GOSUB 기본자세2

        DELAY 1000  '여기에 딜레이 준게 맞는지 확인하기

        GOTO RX_EXIT
    ENDIF
    '**********

연속전진_골프_2:

    MOVE G6A,110,  76, 147,  93, 96,100
    MOVE G6D,90, 90, 120, 105, 110,100
    MOVE G6B,110
    MOVE G6C,90
    WAIT

연속전진_골프_3:
    ETX 4800,11 '진행코드를 보냄

    SPEED 보행속도

    MOVE G6D, 86,  56, 145, 115, 110
    MOVE G6A,108,  76, 147,  93,  96
    WAIT

    SPEED 좌우속도
    MOVE G6D,110,  76, 147, 93,  96
    MOVE G6A,86, 100, 145,  69, 110
    WAIT

    SPEED 보행속도

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO MAIN
    ENDIF

    ERX 4800,A, 연속전진_골프_4
    IF A = 11 THEN
        GOTO 연속전진_골프_4
    ELSE

        MOVE G6A, 90, 100, 100, 115, 110,100
        MOVE G6D,112,  76, 146,  93,  96,100
        MOVE G6B,90
        MOVE G6C,110
        WAIT
        HIGHSPEED SETOFF
        SPEED 8

        MOVE G6D, 106,  76, 146,  93,  96,100		
        MOVE G6A,  88,  71, 152,  91, 106,100
        MOVE G6C, 100
        MOVE G6B, 100
        WAIT	
        SPEED 2
        GOSUB 기본자세2

        GOTO RX_EXIT
    ENDIF

연속전진_골프_4:
    '왼발들기10
    MOVE G6A,90, 90, 120, 105, 110,100
    MOVE G6D,110,  76, 146,  93,  96,100
    MOVE G6B, 90
    MOVE G6C,110
    WAIT

    GOTO 연속전진_골프_1
    '*******************************

    '************************************************
연속후진_골프:
    넘어진확인 = 0
    보행속도 = 12
    좌우속도 = 4
    GOSUB Leg_motor_mode3



    IF 보행순서 = 0 THEN
        보행순서 = 1

        SPEED 4
        MOVE G6A, 88,  71, 152,  91, 110
        MOVE G6D,108,  76, 145,  93,  96
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        SPEED 10
        MOVE G6A, 90, 100, 100, 115, 110
        MOVE G6D,110,  76, 145,  93,  96
        MOVE G6B,90
        MOVE G6C,110
        WAIT

        GOTO 연속후진_골프_1	
    ELSE
        보행순서 = 0

        SPEED 4
        MOVE G6D,  85,  71, 152,  91, 110
        MOVE G6A, 108,  76, 146,  93,  96
        MOVE G6C, 100
        MOVE G6B, 100
        WAIT

        SPEED 10
        MOVE G6D, 90, 100, 100, 115, 110
        MOVE G6A,112,  76, 146,  93,  96
        MOVE G6C,90
        MOVE G6B,110
        WAIT

        GOTO 연속후진_골프_2

    ENDIF

    '*************************************
연속후진_골프_1:
    ETX 4800,12 '진행코드를 보냄
    SPEED 보행속도

    MOVE G6D,110,  76, 146, 93,  96
    MOVE G6A,90, 98, 146,  69, 110
    WAIT

    SPEED 좌우속도
    MOVE G6D, 90,  60, 137, 120, 110
    MOVE G6A,107,  85, 137,  93,  96
    WAIT


    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    SPEED 11

    MOVE G6D,90, 90, 120, 105, 110
    MOVE G6A,112,  76, 146,  93, 96
    MOVE G6B,110
    MOVE G6C,90
    WAIT

    ERX 4800,A, 연속후진_골프_2
    IF A <> A_old THEN
연속후진_골프_1_EXIT:
        HIGHSPEED SETOFF
        SPEED 5

        MOVE G6A, 108,  76, 146,  93,  96		
        MOVE G6D,  85,  72, 148,  91, 106
        MOVE G6B, 100
        MOVE G6C, 100
        WAIT	

        SPEED 3
        GOSUB 기본자세2
        GOTO RX_EXIT
    ENDIF
    '**********

연속후진_골프_2:
    ETX 4800,12 '진행코드를 보냄
    SPEED 보행속도
    MOVE G6A,112,  76, 146, 93,  96
    MOVE G6D,90, 98, 146,  69, 110
    WAIT


    SPEED 좌우속도
    MOVE G6A, 90,  60, 137, 120, 110
    MOVE G6D,107  85, 137,  93,  96
    WAIT


    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF


    SPEED 11
    MOVE G6A,90, 90, 120, 105, 110
    MOVE G6D,110,  76, 146,  93,  96
    MOVE G6B, 90
    MOVE G6C,110
    WAIT


    ERX 4800,A, 연속후진_골프_1
    IF A <> A_old THEN
연속후진_골프_2_EXIT:
        HIGHSPEED SETOFF
        SPEED 5

        MOVE G6D, 106,  76, 146,  93,  96		
        MOVE G6A,  85,  72, 148,  91, 106
        MOVE G6B, 100
        MOVE G6C, 100
        WAIT	

        SPEED 3
        GOSUB 기본자세2
        GOTO RX_EXIT
    ENDIF  	

    GOTO 연속후진_골프_1
    '******************************************
    '******************************************
한걸음:
    MOVE G6A,95,  76, 147,  93, 101
    MOVE G6D,101,  76, 147,  93, 98
    MOVE G6B,100
    MOVE G6C,100
    WAIT

    MOVE G6A,95,  90, 125, 100, 104
    MOVE G6D,103,  76, 146,  93,  102
    MOVE G6B, 90
    MOVE G6C,115
    WAIT

    MOVE G6D,95,  88, 125, 103, 104
    MOVE G6A,107,  76, 146,  93,  102
    MOVE G6C, 85
    MOVE G6B,110
    WAIT



    GOTO RX_EXIT

    '******************************************
전진종종걸음_골프:
    GOSUB All_motor_mode3
    보행COUNT = 0
    SPEED 5
    HIGHSPEED SETON


    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 147,  93, 101
        MOVE G6D,101,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 전진종종걸음_골프_1
    ELSE
        보행순서 = 0
        MOVE G6D,93,  76, 147,  93, 101
        MOVE G6A,104,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 전진종종걸음_골프_4
    ENDIF
    DELAY 3000

    '******************************************

전진종종걸음_골프_1:
    MOVE G6A,95,  90, 125, 100, 104
    MOVE G6D,103,  76, 146,  93,  102
    MOVE G6B, 90
    MOVE G6C,115
    WAIT


전진종종걸음_골프_2:

    MOVE G6A,107,   73, 140, 103,  100
    MOVE G6D, 90,  83, 146,  85, 102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0

        GOTO RX_EXIT
    ENDIF

    ' 보행COUNT = 보행COUNT + 1
    'IF 보행COUNT > 보행횟수 THEN  GOTO 전진종종걸음_골프_2_stop

    ERX 4800,A, 전진종종걸음_골프_4
    IF A <> A_old THEN
전진종종걸음_골프_2_stop:
        MOVE G6D,93,  90, 125, 95, 104
        MOVE G6A,107,  76, 145,  91,  102
        MOVE G6C, 100
        MOVE G6B,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    '*********************************

전진종종걸음_골프_4:
    MOVE G6D,95,  88, 125, 103, 104
    MOVE G6A,107,  76, 146,  93,  102
    MOVE G6C, 85
    MOVE G6B,110
    WAIT


전진종종걸음_골프_5:
    MOVE G6D,102,    74, 140, 103,  100
    MOVE G6A, 97,  83, 146,  85, 102
    WAIT
    'DELAY 10

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    ' 보행COUNT = 보행COUNT + 1
    ' IF 보행COUNT > 보행횟수 THEN  GOTO 전진종종걸음_골프_5_stop

    ERX 4800,A, 전진종종걸음_골프_1
    IF A <> A_old THEN
전진종종걸음_골프_5_stop:
        MOVE G6A,95,  90, 125, 95, 104
        MOVE G6D,104,  76, 145,  91,  102
        MOVE G6B, 100
        MOVE G6C,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    '*************************************

    '*********************************

    GOTO 전진종종걸음_골프_1

    '******************************************
    '******************************************
    '******************************************
후진종종걸음_골프:
    GOSUB All_motor_mode3
    넘어진확인 = 0
    보행COUNT = 0
    SPEED 7
    HIGHSPEED SETON


    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  76, 145,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 후진종종걸음_골프_1
    ELSE
        보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  76, 145,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 후진종종걸음_골프_4
    ENDIF


    '**********************

후진종종걸음_골프_1:
    MOVE G6D,104,  76, 147,  93,  102
    MOVE G6A,95,  95, 120, 95, 104
    MOVE G6B,115
    MOVE G6C,85
    WAIT



후진종종걸음_골프_3:
    MOVE G6A, 103,  79, 147,  89, 100
    MOVE G6D,95,   65, 147, 103,  102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF
    ' 보행COUNT = 보행COUNT + 1
    ' IF 보행COUNT > 보행횟수 THEN  GOTO 후진종종걸음_골프_3_stop

    ERX 4800,A, 후진종종걸음_골프_4
    IF A <> A_old THEN
후진종종걸음_골프_3_stop:
        MOVE G6D,95,  85, 130, 100, 104
        MOVE G6A,104,  77, 146,  93,  102
        MOVE G6C, 100
        MOVE G6B,100
        WAIT

        'SPEED 15
        GOSUB 안정화자세
        HIGHSPEED SETOFF
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF
    '*********************************

후진종종걸음_골프_4:
    MOVE G6A,104,  76, 147,  93,  102
    MOVE G6D,95,  95, 120, 95, 104
    MOVE G6C,115
    MOVE G6B,85
    WAIT


후진종종걸음_골프_6:
    MOVE G6D, 103,  79, 147,  89, 100
    MOVE G6A,95,   65, 147, 103,  102
    WAIT
    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    ' 보행COUNT = 보행COUNT + 1
    'IF 보행COUNT > 보행횟수 THEN  GOTO 후진종종걸음_골프_6_stop

    ERX 4800,A, 후진종종걸음_골프_1
    IF A <> A_old THEN  'GOTO 후진종종걸음_멈춤
후진종종걸음_골프_6_stop:
        MOVE G6A,95,  85, 130, 100, 104
        MOVE G6D,104,  77, 146,  93,  102
        MOVE G6B, 100
        MOVE G6C,100
        WAIT

        'SPEED 15
        GOSUB 안정화자세
        HIGHSPEED SETOFF
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    GOTO 후진종종걸음_골프_1




    '******************************************



    '************************************************
오른쪽옆으로20_골프: '****
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6D, 95,  90, 125, 100, 107, 100
    MOVE G6A,107,  77, 147,  93, 107 , 100
    WAIT

    SPEED 12
    MOVE G6D, 102,  77, 147, 93, 100, 100
    MOVE G6A,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6D,95,  76, 147,  93, 98, 100
    MOVE G6A,95,  76, 147,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT
    '************************************************

왼쪽옆으로20_골프: '****
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6A, 95,  90, 125, 100, 104, 100
    MOVE G6D,105,  76, 146,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6A, 102,  76, 146, 93, 100, 100
    MOVE G6D,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6A,95,  76, 146,  93, 98, 100
    MOVE G6D,95,  76, 146,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************

왼쪽옆으로10_골프: '****
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6A, 97,  90, 123, 100, 104, 100
    MOVE G6D,104,  76, 144,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6A,103,  76, 144, 93, 100, 100
    MOVE G6D,90,  80, 138,  95, 104, 100
    WAIT

    SPEED 12
    MOVE G6A,98	,  76, 144,  93, 98, 100
    MOVE G6D,98,  76, 144,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2
    DELAY 700
    GOTO RX_EXIT

    '**********************************************

오른쪽옆으로10_골프: '****
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6D, 97,  90, 123, 100, 104, 100
    MOVE G6A,104,  76, 144,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6D,103,  76, 144, 93, 100, 100
    MOVE G6A,90,  80, 138,  95, 104, 100
    WAIT

    SPEED 12
    MOVE G6D,98,  76, 144,  93, 98, 100
    MOVE G6A,98,  76, 144,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2
    DELAY 700
    GOTO RX_EXIT

    '**********************************************
    '******************************************
오른쪽옆으로70연속_골프:
    MOTORMODE G6A,3,3,2,3,2
    MOTORMODE G6D,3,3,2,3,2

오른쪽옆으로70연속_골프_loop:
    DELAY  10

    SPEED 10
    MOVE G6D, 90,  90, 120, 105, 110, 100
    MOVE G6A,103,  77, 147,  93, 107, 100
    WAIT

    SPEED 13
    MOVE G6D, 102,  77, 147, 93, 100, 100
    MOVE G6A,83,  77, 140,  96, 115, 100
    WAIT

    SPEED 13
    MOVE G6D,98,  77, 147,  93, 100, 100
    MOVE G6A,98,  77, 147,  93, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,100,  77, 145,  93, 100, 100
    MOVE G6D,100,  77, 145,  93, 100, 100
    WAIT


    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************

왼쪽옆으로70연속_골프:
    MOTORMODE G6A,3,3,2,3,2
    MOTORMODE G6D,3,3,2,3,2
왼쪽옆으로70연속_골프_loop:
    DELAY  10

    SPEED 10
    MOVE G6A, 90,  90, 120, 95, 110, 100	
    MOVE G6D,100,  76, 146,  93, 107, 100	
    WAIT

    SPEED 13
    MOVE G6A, 102,  76, 146, 93, 100, 100
    MOVE G6D,83,  79, 140,  99, 115, 100
    WAIT

    SPEED 13
    MOVE G6A,98,  76, 146,  93, 100, 100
    MOVE G6D,98,  76, 146,  93, 100, 100
    WAIT

    SPEED 12
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6A,100,  76, 145,  93, 100, 100
    WAIT


    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT

    '**********************************************
    '************************************************
    '*********************************************

왼쪽턴3:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
왼쪽턴3_LOOP:

    IF 보행순서 = 0 THEN
        보행순서 = 1
        SPEED 15
        MOVE G6D,100,  73, 145,  93, 100, 100
        MOVE G6A,100,  79, 145,  93, 100, 100
        WAIT

        SPEED 6
        MOVE G6D,100,  84, 145,  78, 100, 100
        MOVE G6A,100,  68, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6D,90,  90, 145,  78, 102, 100
        MOVE G6A,104,  71, 145,  105, 100, 100
        WAIT
        SPEED 7
        MOVE G6D,90,  80, 130, 102, 104
        MOVE G6A,105,  76, 146,  93,  100
        WAIT



    ELSE
        보행순서 = 0
        SPEED 15
        MOVE G6D,100,  73, 145,  93, 100, 100
        MOVE G6A,100,  79, 145,  93, 100, 100
        WAIT


        SPEED 6
        MOVE G6D,100,  88, 145,  78, 100, 100
        MOVE G6A,100,  65, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6D,104,  86, 146,  80, 100, 100
        MOVE G6A,90,  58, 145,  110, 100, 100
        WAIT

        SPEED 7
        MOVE G6A,90,  85, 130, 98, 104
        MOVE G6D,105,  77, 146,  93,  100
        WAIT



    ENDIF

    SPEED 12
    GOSUB 기본자세2


    GOTO RX_EXIT

    '**********************************************
오른쪽턴3:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

오른쪽턴3_LOOP:

    IF 보행순서 = 0 THEN
        보행순서 = 1
        SPEED 15
        MOVE G6A,100,  73, 145,  93, 100, 100
        MOVE G6D,100,  79, 145,  93, 100, 100
        WAIT


        SPEED 6
        MOVE G6A,100,  84, 145,  78, 100, 100
        MOVE G6D,100,  68, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6A,90,  90, 145,  78, 102, 100
        MOVE G6D,104,  71, 145,  105, 100, 100
        WAIT
        SPEED 7
        MOVE G6A,90,  80, 130, 102, 104
        MOVE G6D,105,  76, 146,  93,  100
        WAIT



    ELSE
        보행순서 = 0
        SPEED 15
        MOVE G6A,100,  73, 145,  93, 100, 100
        MOVE G6D,100,  79, 145,  93, 100, 100
        WAIT


        SPEED 6
        MOVE G6A,100,  88, 145,  78, 100, 100
        MOVE G6D,100,  65, 145,  108, 100, 100
        WAIT

        SPEED 9
        MOVE G6A,104,  86, 146,  80, 100, 100
        MOVE G6D,90,  58, 145,  110, 100, 100
        WAIT

        SPEED 7
        MOVE G6D,90,  85, 130, 98, 104
        MOVE G6A,105,  77, 146,  93,  100
        WAIT

    ENDIF
    SPEED 12
    GOSUB 기본자세2

    GOTO RX_EXIT

    '******************************************************
    '**********************************************
왼쪽턴5_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,100,  81, 145,  88, 106, 100
    MOVE G6D,94,  71, 145, 98, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,97,  81, 145,  88, 104, 100
    MOVE G6D,91,  71, 145, 98, 96, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    DELAY 1000
    GOTO RX_EXIT
    '**********************************************
오른쪽턴5_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,97,  71, 145,  98, 103, 100
    MOVE G6D,97,  81, 145,  88, 103, 100
    WAIT

    SPEED 12
    MOVE G6A,94,  71, 145,  98, 101, 100
    MOVE G6D,94,  81, 145,  88, 101, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    DELAY 1000
    GOTO RX_EXIT
    '**********************************************

    '**********************************************
왼쪽턴10_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,100,  86, 145,  83, 106, 100
    MOVE G6D,94,  66, 145, 103, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,97,  86, 145,  83, 104, 100
    MOVE G6D,91,  66, 145, 103, 96, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    GOTO RX_EXIT
    '**********************************************
오른쪽턴10_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,97,  66, 145,  103, 103, 100
    MOVE G6D,97,  86, 145,  83, 103, 100
    WAIT

    SPEED 12
    MOVE G6A,94,  66, 145,  103, 101, 100
    MOVE G6D,94,  86, 145,  83, 101, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************
    '**********************************************
왼쪽턴20_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 8
    MOVE G6A,95,  96, 145,  73, 108, 100
    MOVE G6D,91,  56, 145,  113, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  96, 145,  73, 108, 100
    MOVE G6D,88,  56, 145,  113, 102, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************
오른쪽턴20_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 8
    MOVE G6A,95,  56, 145,  113, 105, 100
    MOVE G6D,95,  96, 145,  73, 105, 100
    WAIT

    SPEED 12
    MOVE G6A,93,  56, 145,  113, 105, 100
    MOVE G6D,93,  96, 145,  73, 105, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100

    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************

    '**********************************************	
왼쪽턴45_골프_연속3:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 10
    MOVE G6A,95,  106, 145,  63, 108, 100
    MOVE G6D,91,  46, 145,  123, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  106, 145,  63, 108, 100
    MOVE G6D,88,  46, 145,  123, 102, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2
    DELAY 500

    SPEED 10
    MOVE G6A,95,  106, 145,  63, 108, 100
    MOVE G6D,91,  46, 145,  123, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  106, 145,  63, 108, 100
    MOVE G6D,88,  46, 145,  123, 102, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2
    DELAY 500

    SPEED 10
    MOVE G6A,95,  106, 145,  63, 108, 100
    MOVE G6D,91,  46, 145,  123, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  106, 145,  63, 108, 100
    MOVE G6D,88,  46, 145,  123, 102, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2
    DELAY 500

    GOTO RX_EXIT

    '**********************************************


왼쪽턴45_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 10
    MOVE G6A,95,  106, 145,  63, 108, 100
    MOVE G6D,91,  46, 145,  123, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  106, 145,  63, 108, 100
    MOVE G6D,88,  46, 145,  123, 102, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2

    '
    GOTO RX_EXIT

    '**********************************************
오른쪽턴45_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 10
    MOVE G6A,95,  46, 145,  123, 105, 100
    MOVE G6D,95,  106, 145,  63, 105, 100
    WAIT

    SPEED 12
    MOVE G6A,93,  46, 145,  123, 105, 100
    MOVE G6D,93,  106, 145,  63, 105, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2

    GOTO RX_EXIT
    '**********************************************
왼쪽턴60_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 15
    MOVE G6A,95,  116, 145,  53, 108, 100
    MOVE G6D,91,  36, 145,  133, 102, 100
    WAIT

    SPEED 15
    MOVE G6A,91,  116, 145,  53, 108, 100
    MOVE G6D,88,  36, 145,  133, 102, 100
    WAIT

    SPEED 10
    GOSUB 기본자세2

    GOTO RX_EXIT

    '**********************************************
오른쪽턴60_골프:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2


    SPEED 15
    MOVE G6A,95,  36, 145,  133, 105, 100
    MOVE G6D,95,  116, 145,  53, 105, 100
    WAIT

    SPEED 15
    MOVE G6A,90,  36, 145,  133, 105, 100
    MOVE G6D,90,  116, 145,  53, 105, 100
    WAIT

    SPEED 10
    GOSUB 기본자세2

    GOTO RX_EXIT
    '****************************************
    '************************************************
    '**********************************************


    '************************************************

    ''************************************************
    '************************************************
    '************************************************
뒤로일어나기:

    HIGHSPEED SETOFF
    PTP SETON 				
    PTP ALLON		

    GOSUB 자이로OFF

    GOSUB All_motor_Reset

    SPEED 15
    GOSUB 기본자세

    MOVE G6A,90, 130, 120,  80, 110, 100
    MOVE G6D,90, 130, 120,  80, 110, 100
    MOVE G6B,150, 160,  10, 100, 100, 100
    MOVE G6C,150, 160,  10, 190, 100, 100
    WAIT

    MOVE G6B,185, 160,  10, 100, 100, 100
    MOVE G6C,185, 160,  10, 190, 100, 100
    WAIT

    SPEED 12
    MOVE G6B,185,  50, 10,  100, 100, 100
    MOVE G6C,185,  50, 10,  190, 100, 100
    WAIT



    SPEED 10
    MOVE G6A, 80, 155,  80, 150, 150, 100
    MOVE G6D, 80, 155,  80, 150, 150, 100
    MOVE G6B,185,  20, 50,  100, 100, 100
    MOVE G6C,185,  20, 50,  190, 100, 100
    WAIT

    MOVE G6A, 75, 162,  55, 162, 155, 100
    MOVE G6D, 75, 162,  55, 162, 155, 100
    MOVE G6B,188,  10, 100, 100, 100, 100
    MOVE G6C,188,  10, 100, 190, 100, 100
    WAIT

    SPEED 10
    MOVE G6A, 60, 162,  30, 162, 145, 100
    MOVE G6D, 60, 162,  30, 162, 145, 100
    MOVE G6B,170,  10, 100, 100, 100, 100
    MOVE G6C,170,  10, 100, 190, 100, 100
    WAIT

    DELAY 200


    GOSUB Leg_motor_mode3	
    MOVE G6A, 60, 150,  28, 155, 140, 100
    MOVE G6D, 60, 150,  28, 155, 140, 100
    MOVE G6B,150,  60,  90, 100, 100, 100
    MOVE G6C,150,  60,  90, 190, 100, 100
    WAIT

    MOVE G6A,100, 150,  28, 140, 100, 100
    MOVE G6D,100, 150,  28, 140, 100, 100
    MOVE G6B,130,  50,  85, 100, 100, 100
    MOVE G6C,130,  50,  85, 190, 100, 100
    WAIT
    DELAY 100

    MOVE G6A,100, 150,  33, 140, 100, 100
    MOVE G6D,100, 150,  33, 140, 100, 100
    WAIT
    SPEED 10
    GOSUB 기본자세

    넘어진확인 = 1

    DELAY 200
    GOSUB 자이로ON

    RETURN


    '**********************************************
앞으로일어나기:


    HIGHSPEED SETOFF
    PTP SETON 				
    PTP ALLON

    GOSUB 자이로OFF

    HIGHSPEED SETOFF

    GOSUB All_motor_Reset

    SPEED 15
    MOVE G6A,100, 35,  70, 130, 100,
    MOVE G6D,100, 35,  70, 130, 100,
    MOVE G6B,15,  140,  15
    MOVE G6C,15,  140,  15
    WAIT

    SPEED 12
    MOVE G6B,15,  100,  10
    MOVE G6C,15,  100,  10
    WAIT

    SPEED 12
    MOVE G6A,100, 136,  35, 80, 100,
    MOVE G6D,100, 136,  35, 80, 100,
    MOVE G6B,15,  15,  75
    MOVE G6C,15,  15,  75
    WAIT

    SPEED 10
    MOVE G6A,100, 165,  75, 20, 100,
    MOVE G6D,100, 165,  75, 20, 100,
    MOVE G6B,15,  20,  95
    MOVE G6C,15,  20,  95
    WAIT

    DELAY 200

    GOSUB Leg_motor_mode3

    SPEED 8
    MOVE G6A,100, 165,  85, 20, 100,
    MOVE G6D,100, 165,  85, 20, 100,
    MOVE G6B,130,  50,  60
    MOVE G6C,130,  50,  60
    WAIT

    SPEED 8
    MOVE G6A,100, 165,  85, 30, 100,
    MOVE G6D,100, 165,  85, 30, 100,
    WAIT

    SPEED 8
    MOVE G6A,100, 155,  45, 110, 100,
    MOVE G6D,100, 155,  45, 110, 100,
    MOVE G6B,130,  50,  60
    MOVE G6C,130,  50,  60
    WAIT

    SPEED 6
    MOVE G6A,100, 145,  45, 130, 100,
    MOVE G6D,100, 145,  45, 130, 100,
    WAIT


    SPEED 8
    GOSUB All_motor_mode2
    GOSUB 기본자세
    넘어진확인 = 1

    '******************************
    DELAY 200
    GOSUB 자이로ON
    RETURN

    '******************************************
    '******************************************
    '******************************************
    '**************************************************

    '******************************************
    '******************************************	
    '**********************************************

머리왼쪽30도:
    SPEED 머리이동속도
    SERVO 11,70
    GOTO RX_EXIT


머리왼쪽60도:
    SPEED 머리이동속도
    SERVO 11,40
    GOTO RX_EXIT
    '*****************************************************
호우_세레머니:
    'MOVE G6A,100,  76, 145,  93, 100, 100
    'MOVE G6D,100,  76, 145,  93, 100, 100
    'MOVE G6B,100,  30,  80,
    'MOVE G6C,100,  30,  80, 190
    'WAIT
    SPEED 10
    MOVE G6A,100, 145,  45, 130, 100, 100
    MOVE G6D,100, 145,  45, 130, 100, 100
    MOVE G6B,190,  30,  80,
    MOVE G6C,190,  30,  80, 190
    WAIT

    SPEED 13
    MOVE G6A,100,  110, 95,  111, 100, 100
    MOVE G6D,100,  110, 95,  111, 100, 100
    MOVE G6B,130,  30,  80,
    MOVE G6C,130,  30,  80, 190
    WAIT

    SPEED 13
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,80,  45,  100,
    MOVE G6C,80,  45,  100, 190
    WAIT

    GOTO RX_EXIT

    '*****************************************************
공찾기_왼쪽:
    '머리왼쪽90도:
    SPEED 머리이동속도
    SERVO 11,10
    WAIT
    DELAY 300

    '머리왼쪽81도:
    SPEED 머리이동속도
    SERVO 11,19
    WAIT
    DELAY 300

    '머리왼쪽72도:
    SPEED 머리이동속도
    SERVO 11,28
    WAIT
    DELAY 300

    '머리왼쪽63도:
    SPEED 머리이동속도
    SERVO 11,37
    WAIT
    DELAY 300

    '머리왼쪽54도:
    SPEED 머리이동속도
    SERVO 11,46
    WAIT
    DELAY 300

    '머리왼쪽45도:
    SPEED 머리이동속도
    SERVO 11,55
    WAIT
    DELAY 300

    '머리왼쪽36도:
    SPEED 머리이동속도
    SERVO 11,64
    WAIT
    DELAY 300

    '머리왼쪽27도:
    SPEED 머리이동속도
    SERVO 11,73
    WAIT
    DELAY 300

    '머리왼쪽18도:
    SPEED 머리이동속도
    SERVO 11,82
    WAIT
    DELAY 300

    '머리왼쪽9도:
    SPEED 머리이동속도
    SERVO 11,91
    WAIT
    DELAY 300

    '머리좌우중앙:
    SPEED 머리이동속도
    SERVO 11,100
    WAIT
    DELAY 300
    GOTO RX_EXIT

    '*********************************************************************
공찾기_오른쪽:
    '머리오른쪽9도:
    SPEED 머리이동속도
    SERVO 11,109
    GOTO RX_EXIT

    '머리오른쪽18도:
    SPEED 머리이동속도
    SERVO 11,118
    GOTO RX_EXIT

    '머리오른쪽27도:
    SPEED 머리이동속도
    SERVO 11,127
    GOTO RX_EXIT

    '머리오른쪽36도:
    SPEED 머리이동속도
    SERVO 11,136
    GOTO RX_EXIT

    '머리오른쪽45도:
    SPEED 머리이동속도
    SERVO 11,145
    GOTO RX_EXIT

    '머리오른쪽54도:
    SPEED 머리이동속도
    SERVO 11,154
    GOTO RX_EXIT	

    '머리오른쪽63도:
    SPEED 머리이동속도
    SERVO 11,163
    GOTO RX_EXIT

    '머리오른쪽72도:
    SPEED 머리이동속도
    SERVO 11,172
    GOTO RX_EXIT

    '머리오른쪽81도:
    SPEED 머리이동속도
    SERVO 11,181
    GOTO RX_EXIT

    '머리오른쪽90도:
    SPEED 머리이동속도
    SERVO 11,190
    GOTO RX_EXIT

    '*****************************************************
머리왼쪽90도:
    SPEED 머리이동속도
    SERVO 11,10
    GOTO RX_EXIT

머리왼쪽81도:
    SPEED 머리이동속도
    SERVO 11,19
    GOTO RX_EXIT

머리왼쪽78도:
    SPEED 머리이동속도
    SERVO 11,22
    GOTO RX_EXIT
머리왼쪽72도:
    SPEED 머리이동속도
    SERVO 11,28
    GOTO RX_EXIT

머리왼쪽63도:
    SPEED 머리이동속도
    SERVO 11,37
    GOTO RX_EXIT

머리왼쪽54도:
    SPEED 머리이동속도
    SERVO 11,46
    GOTO RX_EXIT

머리왼쪽45도:
    SPEED 머리이동속도
    SERVO 11,55
    GOTO RX_EXIT

머리왼쪽36도:
    SPEED 머리이동속도
    SERVO 11,64
    GOTO RX_EXIT

머리왼쪽27도:
    SPEED 머리이동속도
    SERVO 11,73
    GOTO RX_EXIT

머리왼쪽18도:
    SPEED 머리이동속도
    SERVO 11,82
    GOTO RX_EXIT

머리왼쪽9도:
    SPEED 머리이동속도
    SERVO 11,91
    GOTO RX_EXIT

머리좌우중앙:
    SPEED 머리이동속도
    SERVO 11,100
    GOTO RX_EXIT

머리오른쪽9도:
    SPEED 머리이동속도
    SERVO 11,109
    GOTO RX_EXIT

머리오른쪽18도:
    SPEED 머리이동속도
    SERVO 11,118
    GOTO RX_EXIT

머리오른쪽27도:
    SPEED 머리이동속도
    SERVO 11,127
    GOTO RX_EXIT

머리오른쪽36도:
    SPEED 머리이동속도
    SERVO 11,136
    GOTO RX_EXIT

머리오른쪽45도:
    SPEED 머리이동속도
    SERVO 11,145
    GOTO RX_EXIT

머리오른쪽54도:
    SPEED 머리이동속도
    SERVO 11,154
    GOTO RX_EXIT	

머리오른쪽63도:
    SPEED 머리이동속도
    SERVO 11,163
    GOTO RX_EXIT

머리오른쪽72도:
    SPEED 머리이동속도
    SERVO 11,172
    GOTO RX_EXIT

머리오른쪽81도:
    SPEED 머리이동속도
    SERVO 11,181
    GOTO RX_EXIT

머리오른쪽60도:
    SPEED 머리이동속도
    SERVO 11,160
    GOTO RX_EXIT

머리오른쪽90도:
    SPEED 머리이동속도
    SERVO 11,190
    GOTO RX_EXIT

    '**************************************************************

뉴전방하향90도:
    SPEED 5
    SERVO 16, 100
    DELAY 500
    GOTO RX_EXIT

뉴전방하향80도:
    SPEED 5
    SERVO 16, 90
    DELAY 500
    GOTO RX_EXIT

뉴전방하향70도:
    SPEED 5
    SERVO 16, 80
    DELAY 500
    GOTO RX_EXIT

뉴전방하향60도:
    SPEED 5
    SERVO 16, 70
    DELAY 500
    GOTO RX_EXIT

뉴전방하향50도:
    SPEED 5
    SERVO 16, 60
    DELAY 500
    GOTO RX_EXIT

뉴전방하향40도:
    SPEED 5
    SERVO 16, 50
    DELAY 500
    GOTO RX_EXIT

뉴전방하향30도:
    SPEED 5
    SERVO 16, 40
    DELAY 500
    GOTO RX_EXIT

뉴전방하향20도:
    SPEED 5
    SERVO 16, 30
    DELAY 500
    GOTO RX_EXIT

    '**************************************************************




머리상하정면:
    SPEED 머리이동속도
    SERVO 16,100	
    GOTO RX_EXIT

전방하향90도:
    SPEED 5
    SERVO 16, 100
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

전방하향80도:
    SPEED 5
    SERVO 16, 90
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

전방하향70도:
    SPEED 5
    SERVO 16, 80
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

전방하향60도:
    SPEED 5
    SERVO 16, 70
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

전방하향50도:
    SPEED 5
    SERVO 16, 60
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

전방하향40도:
    SPEED 5
    SERVO 16, 50
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

전방하향30도:
    SPEED 5
    SERVO 16, 40
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

전방하향20도:
    SPEED 5
    SERVO 16, 30
    SERVO 11, 100
    DELAY 500
    GOTO RX_EXIT

    '******************************************

    '******************************************
앞뒤기울기측정:
    FOR i = 0 TO COUNT_MAX
        A = AD(앞뒤기울기AD포트)	'기울기 앞뒤
        IF A > 250 OR A < 5 THEN RETURN
        IF A > MIN AND A < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF A < MIN THEN
        GOSUB 기울기앞
    ELSEIF A > MAX THEN
        GOSUB 기울기뒤
    ENDIF

    RETURN
    '**************************************************
기울기앞:
    A = AD(앞뒤기울기AD포트)
    'IF A < MIN THEN GOSUB 앞으로일어나기
    IF A < MIN THEN
        ETX  4800,16
        GOSUB 뒤로일어나기

    ENDIF
    RETURN

기울기뒤:
    A = AD(앞뒤기울기AD포트)
    'IF A > MAX THEN GOSUB 뒤로일어나기
    IF A > MAX THEN
        ETX  4800,15
        GOSUB 앞으로일어나기
    ENDIF
    RETURN
    '**************************************************
좌우기울기측정:
    FOR i = 0 TO COUNT_MAX
        B = AD(좌우기울기AD포트)	'기울기 좌우
        IF B > 250 OR B < 5 THEN RETURN
        IF B > MIN AND B < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF B < MIN OR B > MAX THEN
        SPEED 8
        MOVE G6B,140,  40,  80
        MOVE G6C,140,  40,  80
        WAIT
        GOSUB 기본자세	
    ENDIF
    RETURN
    '******************************************
    '************************************************
SOUND_PLAY_CHK:
    DELAY 60
    SOUND_BUSY = IN(46)
    IF SOUND_BUSY = 1 THEN GOTO SOUND_PLAY_CHK
    DELAY 50

    RETURN
    '************************************************

    '************************************************
NUM_1_9:
    IF NUM = 1 THEN
        PRINT "1"
    ELSEIF NUM = 2 THEN
        PRINT "2"
    ELSEIF NUM = 3 THEN
        PRINT "3"
    ELSEIF NUM = 4 THEN
        PRINT "4"
    ELSEIF NUM = 5 THEN
        PRINT "5"
    ELSEIF NUM = 6 THEN
        PRINT "6"
    ELSEIF NUM = 7 THEN
        PRINT "7"
    ELSEIF NUM = 8 THEN
        PRINT "8"
    ELSEIF NUM = 9 THEN
        PRINT "9"
    ELSEIF NUM = 0 THEN
        PRINT "0"
    ENDIF

    RETURN
    '************************************************
    '************************************************
NUM_TO_ARR:

    NO_4 =  BUTTON_NO / 10000
    TEMP_INTEGER = BUTTON_NO MOD 10000

    NO_3 =  TEMP_INTEGER / 1000
    TEMP_INTEGER = BUTTON_NO MOD 1000

    NO_2 =  TEMP_INTEGER / 100
    TEMP_INTEGER = BUTTON_NO MOD 100

    NO_1 =  TEMP_INTEGER / 10
    TEMP_INTEGER = BUTTON_NO MOD 10

    NO_0 =  TEMP_INTEGER

    RETURN
    '************************************************
Number_Play: '  BUTTON_NO = 숫자대입


    GOSUB NUM_TO_ARR

    PRINT "NPL "
    '*************

    NUM = NO_4
    GOSUB NUM_1_9

    '*************
    NUM = NO_3
    GOSUB NUM_1_9

    '*************
    NUM = NO_2
    GOSUB NUM_1_9
    '*************
    NUM = NO_1
    GOSUB NUM_1_9
    '*************
    NUM = NO_0
    GOSUB NUM_1_9
    PRINT " !"

    ' GOSUB SOUND_PLAY_CHK
    '    PRINT "SND 16 !"
    '    GOSUB SOUND_PLAY_CHK
    RETURN
    '************************************************

    RETURN


    '******************************************

    ' ************************************************
적외선거리센서확인:

    적외선거리값 = AD(적외선AD포트)

    IF 적외선거리값 > 50 THEN '50 = 적외선거리값 = 25cm
        MUSIC "C"
        DELAY 200
    ENDIF


    RETURN

    '******************************************
변수값_음성값출력:

    J = AD(적외선AD포트)	'적외선거리값 읽기
    BUTTON_NO = J
    GOSUB Number_Play
    GOSUB SOUND_PLAY_CHK
    GOSUB GOSUB_RX_EXIT


    RETURN

    '************************************************
골프_샷준비:

    SPEED 8
    MOVE G6C,135,  10,  70, 10
    WAIT
    DELAY 500

    RETURN

    '************************************************
골프_왼쪽으로_샷1:

    CONST 골프채높이 = 135

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT

    DELAY 400


    MOVE G6C,135,  40,  90, 10
    WAIT

    '**** 골프 _왼쪽으로_샷 스피드 *******
    'HIGHSPEED SETON
    SPEED 8
    MOVE G6C,135,  10,  70, 10
    WAIT
    DELAY 1000
    ' HIGHSPEED SETOFF

    '************

    SPEED 8
    MOVE G6C,135,  100,  10, 10
    WAIT

    MOVE G6C,135,  50,  60, 190
    WAIT

    GOSUB 기본자세

    RETURN
    '***********************************************
골프_왼쪽으로_샷2:
    CONST 골프채높이1 = 135

    SPEED 5
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT

    DELAY 400

    MOVE G6C,135,  40,  90, 10
    WAIT

    '**** 골프 _왼쪽으로_샷 스피드 *******
    'HIGHSPEED SETON
    SPEED 5
    MOVE G6C,135,  10,  70, 10
    WAIT
    DELAY 1000
    ' HIGHSPEED SETOFF


    SPEED 5
    MOVE G6C,135,  100,  10, 10
    WAIT

    MOVE G6C,135,  50,  60, 190
    WAIT

    GOSUB 기본자세

    RETURN
    '************************************************

골프_왼쪽으로_어드레스1:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT


    MOVE G6C,135,  20,  90, 10
    WAIT

    RETURN
    '******************************************
동심원_왼쪽으로:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6A, 95,  90, 125, 100, 104, 100
    MOVE G6D,105,  76, 146,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6A, 102,  76, 146, 93, 100, 100
    MOVE G6D,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6A,95,  76, 146,  93, 98, 100
    MOVE G6D,95,  76, 146,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    SPEED 12
    MOVE G6A, 95,  90, 125, 100, 104, 100
    MOVE G6D,105,  76, 146,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6A, 102,  76, 146, 93, 100, 100
    MOVE G6D,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6A,95,  76, 146,  93, 98, 100
    MOVE G6D,95,  76, 146,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    SPEED 8
    MOVE G6D,95,  91, 145,  78, 107, 100
    MOVE G6A,91,  61, 145,  108, 101, 100
    WAIT

    SPEED 12
    MOVE G6D,91,  91, 145,  78, 106, 100
    MOVE G6A,88,  61, 145,  108, 100, 100
    WAIT
    SPEED 6
    MOVE G6D,101,  76, 146,  93, 98, 100
    MOVE G6A,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    DELAY 1000
    GOTO RX_EXIT
    '************************************************
동심원_오른쪽으로:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6D, 95,  90, 125, 100, 104, 100
    MOVE G6A,105,  76, 146,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6D, 102,  76, 146, 93, 100, 100
    MOVE G6A,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6D,95,  76, 146,  93, 98, 100
    MOVE G6A,95,  76, 146,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    SPEED 12
    MOVE G6D, 95,  90, 125, 100, 104, 100
    MOVE G6A,105,  76, 146,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6D, 102,  76, 146, 93, 100, 100
    MOVE G6A,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6D,95,  76, 146,  93, 98, 100
    MOVE G6A,95,  76, 146,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    SPEED 8
    MOVE G6A,95,  91, 145,  78, 107, 100
    MOVE G6D,91,  61, 145,  108, 101, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  91, 145,  78, 106, 100
    MOVE G6D,88,  61, 145,  108, 100, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    DELAY 1000
    GOTO RX_EXIT
    '************************************************
골프_오른쪽으로_샷1:

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  130,  10, 10
    WAIT

    MOVE G6C,145,  130,  10, 10
    WAIT

    MOVE G6C,145,  60,  10, 10
    WAIT

    MOVE G6C,135,  40,  30, 10
    WAIT


    MOVE G6C,140,  10,  80, 10
    WAIT

    DELAY 400

    MOVE G6B,100,  35,  90,
    MOVE G6C,140,  10,  70, 10
    WAIT

    '**** 골프 _오른쪽으로_샷 스피드 *******
    'HIGHSPEED SETON
    SPEED 3

    MOVE G6C,140,  30,  100, 10
    WAIT
    DELAY 1000
    ' HIGHSPEED SETOFF

    '************

    SPEED 8
    MOVE G6C,135,  50,  60, 190
    WAIT

    GOSUB 기본자세

    RETURN
    '******************************************


골프_오른쪽으로_어드레스1:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT


    MOVE G6C,135,  40,  40, 10
    WAIT

    MOVE G6C,135,  10,  80, 10
    WAIT


    RETURN
    '******************************************
    '******************************************	
MAIN: '라벨설정

    'ETX 4800, 38 ' 동작 멈춤 확인 송신 값                                           원래 주석 아니였음

MAIN_2:

    GOSUB 앞뒤기울기측정
    GOSUB 좌우기울기측정
    'GOSUB 적외선거리센서확인


    ERX 4800,A,MAIN_2	

    A_old = A

    '**** 입력된 A값이 0 이면 MAIN 라벨로 가고
    '**** 1이면 KEY1 라벨, 2이면 key2로... 가는문
    ON A GOTO MAIN,KEY1,KEY2,KEY3,KEY4,KEY5,KEY6,KEY7,KEY8,KEY9,KEY10,KEY11,KEY12,KEY13,KEY14,KEY15,KEY16,KEY17,KEY18 ,KEY19,KEY20,KEY21,KEY22,KEY23,KEY24,KEY25,KEY26,KEY27,KEY28 ,KEY29,KEY30,KEY31,KEY32, KEY33, KEY34, KEY35, KEY36, KEY37, KEY38, KEY39, KEY40, KEY41, KEY42, KEY43, KEY44, KEY45, KEY46, KEY47, KEY48, KEY49, KEY50, KEY51, KEY52, KEY53, KEY54, KEY55, KEY56, KEY57, KEY58, KEY59, KEY60, KEY61, KEY62, KEY63, KEY64, KEY65, KEY66, KEY67, KEY68, KEY69, KEY70, KEY71, KEY72, KEY73, KEY74, KEY75, KEY76, KEY77, KEY78, KEY79, KEY80, KEY81, KEY82, KEY83, KEY84
    IF A > 100 AND A < 110 THEN
        BUTTON_NO = A - 100





        GOSUB Number_Play
        GOSUB SOUND_PLAY_CHK
        GOSUB GOSUB_RX_EXIT


    ELSEIF A = 250 THEN
        GOSUB All_motor_mode3
        SPEED 4
        MOVE G6A,100,  76, 145,  93, 100, 100
        MOVE G6D,100,  76, 145,  93, 100, 100
        MOVE G6B,100,  40,  90,
        MOVE G6C,100,  40,  90,
        WAIT
        DELAY 500
        SPEED 6
        GOSUB 기본자세

    ENDIF


    GOTO MAIN
    '*******************************************
    '		MAIN 라벨로 가기
    '*******************************************


KEY1:
    'ETX 4800,1
    'GOTO 왼쪽턴45_골프_연속3
    'GOTO RX_EXIT

    ETX 4800,1
    GOTO 골프_왼쪽으로_샷2
    GOTO RX_EXIT

    '***************	
KEY2:
    'ETX 4800,2
    'GOTO 호우_세레머니
    'GOTO RX_EXIT
    ETX 4800,2
    GOTO 왼쪽옆으로10_골프
    GOTO RX_EXIT
    '***************
KEY3:
    ETX 4800,3
    GOTO 오른쪽옆으로10_골프
    GOTO RX_EXIT
    '***************
KEY4:
    ETX 4800,4
    GOTO 왼쪽턴10_골프
    GOTO RX_EXIT
    '***************
KEY5:
    ETX 4800,5
    GOTO 오른쪽턴10_골프
    GOTO RX_EXIT
    '***************
KEY6:
    ETX 4800,6
    GOTO 머리왼쪽78도
    GOTO RX_EXIT
    '***************
KEY7:
    ETX  4800,7
    GOTO 왼쪽턴20_골프
    GOTO RX_EXIT
    '***************
KEY8:
    ETX  4800,8
    GOTO RX_EXIT
    '***************
KEY9:
    ETX  4800,9
    GOTO 오른쪽턴20_골프
    GOTO RX_EXIT
    '***************
KEY10: '0
    ETX  4800,10
    GOTO 전진종종걸음_골프
    GOTO RX_EXIT
    '***************
KEY11: ' ▲
    ETX  4800,11
    GOTO 연속전진_골프
    GOTO RX_EXIT
    '***************
KEY12: ' ▼
    ETX  4800,12
    GOTO 연속후진_골프
    GOTO RX_EXIT
    '***************
KEY13: '▶
    ETX  4800,13
    GOTO 오른쪽옆으로70연속_골프
    GOTO RX_EXIT
    '***************
KEY14: ' ◀
    ETX  4800,14
    GOTO 왼쪽옆으로70연속_골프
    GOTO RX_EXIT
    '***************
KEY15: ' A
    ETX  4800,15
    GOTO 왼쪽옆으로20_골프
    GOTO RX_EXIT
    '***************
KEY16: ' POWER
    ETX  4800,16
    GOSUB Leg_motor_mode3
    IF MODE = 0 THEN
        SPEED 10
        MOVE G6A,100, 140,  37, 145, 100, 100
        MOVE G6D,100, 140,  37, 145, 100, 100
        WAIT
    ENDIF
    SPEED 4
    GOSUB 앉은자세	
    GOSUB 종료음
    GOSUB MOTOR_GET
    GOSUB MOTOR_OFF
    GOSUB GOSUB_RX_EXIT
KEY16_1:

    IF 모터ONOFF = 1  THEN
        OUT 52,1
        DELAY 200
        OUT 52,0
        DELAY 200
    ENDIF
    ERX 4800,A,KEY16_1
    ETX  4800,A

    '**** RX DATA Number Sound ********
    BUTTON_NO = A
    GOSUB Number_Play
    GOSUB SOUND_PLAY_CHK


    IF  A = 16 THEN 	'다시 파워버튼을 눌러야만 복귀
        GOSUB MOTOR_ON
        SPEED 10
        MOVE G6A,100, 140,  37, 145, 100, 100
        MOVE G6D,100, 140,  37, 145, 100, 100
        WAIT

        GOSUB 기본자세2
        GOSUB 자이로ON
        GOSUB All_motor_mode3
        GOTO RX_EXIT
    ENDIF

    GOSUB GOSUB_RX_EXIT
    GOTO KEY16_1


    GOTO RX_EXIT
    '***************
KEY17: ' C
    ETX  4800,17
    GOTO 머리왼쪽90도


    GOTO RX_EXIT
    '***************
KEY18: ' E
    ETX  4800,18	


    GOSUB 자이로OFF
    GOSUB 에러음
KEY18_wait:

    ERX 4800,A,KEY18_wait	

    IF  A = 26 THEN
        GOSUB 시작음
        GOSUB 자이로ON
        GOTO RX_EXIT
    ENDIF

    GOTO KEY18_wait


    GOTO RX_EXIT
    '***************
KEY19: ' P2
    ETX  4800,19
    GOTO 오른쪽턴60_골프

    GOTO RX_EXIT
    '***************
KEY20: ' B	
    ETX  4800,20
    GOTO 오른쪽옆으로20_골프


    GOTO RX_EXIT
    '***************
KEY21: ' △
    ETX  4800,21
    GOTO 머리좌우중앙

    GOTO RX_EXIT
    '***************
KEY22: ' *	
    ETX  4800,22
    GOTO 왼쪽턴45_골프

    GOTO RX_EXIT
    '***************
KEY23: ' G
    ETX  4800,23
    GOTO RX_EXIT
    '***************
KEY24: ' #
    ETX  4800,24
    GOTO 오른쪽턴45_골프

    GOTO RX_EXIT
    '***************
KEY25: ' P1
    ETX  4800,25
    GOTO 왼쪽턴60_골프

    GOTO RX_EXIT
    '***************
KEY26: ' ■
    ETX  4800,26

    SPEED 5
    GOSUB 기본자세2	
    TEMPO 220
    MUSIC "ff"
    GOSUB 기본자세
    GOTO RX_EXIT
    '***************
KEY27: ' D
    ETX  4800,27
    GOTO 머리오른쪽90도
    GOTO RX_EXIT
    '***************
KEY28: ' ◁
    ETX  4800,28
    GOTO 머리왼쪽45도
    GOTO RX_EXIT
    '***************
KEY29: ' □
    ETX  4800,29
    GOTO 전방하향80도
    GOTO RX_EXIT
    '***************
KEY30: ' ▷
    ETX  4800,30
    GOTO 머리오른쪽45도
    GOTO RX_EXIT
    '***************
KEY31: ' ▽
    ETX  4800,31
    GOTO 전방하향60도
    GOTO RX_EXIT
    '***************

KEY32: ' F
    ETX  4800,32
    GOTO 후진종종걸음_골프
    GOTO RX_EXIT
    '***************

KEY33:
    ETX 4800,33
    GOTO 전방하향30도
    GOTO RX_EXIT
    '***************

KEY34:
    ETX 4800,34
    GOTO 전방하향50도
    GOTO RX_EXIT
    '***************

KEY35:
    ETX 4800,35
    GOTO 전방하향90도
    GOTO RX_EXIT
    '***************

KEY36:
    ETX 4800,36
    GOTO 전방하향70도
    GOTO RX_EXIT
    '***************

KEY37:
    ETX 4800,37
    GOTO 전방하향40도
    GOTO RX_EXIT
    '***************

KEY38:
    ETX 4800,38
    GOTO 전방하향30도
    GOTO RX_EXIT
    '***************

KEY39:
    ETX 4800,39
    GOTO 전방하향20도
    GOTO RX_EXIT
    '***************

KEY40:
    ETX 4800,40
    GOTO 전방하향80도
    GOTO RX_EXIT
    '***************

KEY41:
    ETX 4800,41
    GOTO 왼쪽옆으로10_골프
    GOTO RX_EXIT
    '***************

KEY42:
    ETX 4800,42
    GOTO 오른쪽옆으로10_골프
    GOTO RX_EXIT
    '***************

KEY43:
    ETX 4800,43
    GOTO 동심원_왼쪽으로
    GOTO RX_EXIT
    '***************

KEY44:
    ETX 4800,44
    GOTO 동심원_오른쪽으로
    GOTO RX_EXIT
    '***************

KEY45:
    ETX 4800,45
    GOTO 골프_왼쪽으로_샷2
    GOTO RX_EXIT
    '***************

KEY46:
    ETX 4800,46
    GOTO 머리왼쪽81도
    GOTO RX_EXIT
    '***************

KEY47:
    ETX 4800,47
    GOTO 머리왼쪽72도
    GOTO RX_EXIT
    '***************

KEY48:
    ETX 4800,48
    GOTO 머리왼쪽63도
    GOTO RX_EXIT
    '***************

KEY49:
    ETX 4800,49
    GOTO 머리왼쪽54도
    GOTO RX_EXIT
    '***************

KEY50:
    ETX 4800,50
    GOTO 머리왼쪽45도
    GOTO RX_EXIT
    '***************

KEY51:
    ETX 4800,51
    GOTO 머리왼쪽36도
    GOTO RX_EXIT
    '***************

KEY52:
    ETX 4800,52
    GOTO 머리왼쪽27도
    GOTO RX_EXIT
    '***************

KEY53:
    ETX 4800,53
    GOTO 머리왼쪽18도
    GOTO RX_EXIT
    '***************

KEY54:
    ETX 4800,54
    GOTO 머리왼쪽9도
    GOTO RX_EXIT
    '***************

KEY55:
    ETX 4800,55
    GOTO 머리좌우중앙
    GOTO RX_EXIT
    '***************

KEY56:
    ETX 4800,56
    GOTO 머리오른쪽9도
    GOTO RX_EXIT
    '***************

KEY57:
    ETX 4800,57
    GOTO 머리오른쪽18도
    GOTO RX_EXIT
    '***************

KEY58:
    ETX 4800,58
    GOTO 머리오른쪽27도
    GOTO RX_EXIT
    '***************

KEY59:
    ETX 4800,59
    GOTO 머리오른쪽36도
    GOTO RX_EXIT
    '***************

KEY60:
    ETX 4800,60
    GOTO 머리오른쪽45도
    GOTO RX_EXIT
    '***************

KEY61:
    ETX 4800,61
    GOTO 머리오른쪽54도
    GOTO RX_EXIT
    '***************

KEY62:
    ETX 4800,62
    GOTO 머리오른쪽63도
    GOTO RX_EXIT
    '***************

KEY63:
    ETX 4800,63
    GOTO 머리오른쪽72도
    GOTO RX_EXIT
    '***************

KEY64:
    ETX 4800,64
    GOTO 머리오른쪽81도
    GOTO RX_EXIT
    '***************

KEY65:
    ETX 4800,65
    GOTO 머리오른쪽90도
    GOTO RX_EXIT
    '***************

KEY66:
    ETX 4800,66
    GOTO 골프_샷준비
    GOTO RX_EXIT
    '***************

KEY67:
    ETX  4800,1
    GOTO 왼쪽턴5_골프
    GOTO RX_EXIT
    '***************

KEY68:
    ETX  4800,2
    GOSUB 골프_왼쪽으로_샷1
    GOTO RX_EXIT
    '***************

KEY69:
    ETX  4800,3
    GOTO 오른쪽턴5_골프
    GOTO RX_EXIT
    '***************

KEY70:
    ETX  4800,4
    GOTO 왼쪽턴10_골프
    GOTO RX_EXIT
    '***************

KEY71:
    ETX  4800,5
    GOSUB 골프_오른쪽으로_샷1
    GOTO RX_EXIT
    '***************

KEY72:
    ETX  4800,6
    GOTO 오른쪽턴10_골프
    GOTO RX_EXIT
    '***************

KEY73:
    ETX 4800,73
    GOTO 머리왼쪽78도
    GOTO RX_EXIT
    '***************

KEY74:
    ETX 4800,74
    GOTO 공찾기_왼쪽
    GOTO RX_EXIT
    '***************

KEY75:
    ETX 4800,75
    GOTO 왼쪽턴45_골프_연속3
    GOTO RX_EXIT
    '***************

KEY76:
    ETX 4800,76
    GOTO 호우_세레머니
    GOTO RX_EXIT
    '***************

KEY77:
    ETX 4800,77
    GOTO 뉴전방하향90도
    GOTO RX_EXIT
    '***************

KEY78:
    ETX 4800,78
    GOTO 뉴전방하향80도
    GOTO RX_EXIT
    '***************

KEY79:
    ETX 4800,79
    GOTO 뉴전방하향70도
    GOTO RX_EXIT
    '***************

KEY80:
    ETX 4800,80
    GOTO 뉴전방하향60도
    GOTO RX_EXIT
    '***************

KEY81:
    ETX 4800,81
    GOTO 뉴전방하향50도
    GOTO RX_EXIT
    '***************

KEY82:
    ETX 4800,82
    GOTO 뉴전방하향40도
    GOTO RX_EXIT
    '***************

KEY83:
    ETX 4800,83
    GOTO 뉴전방하향30도
    GOTO RX_EXIT
    '***************

KEY84:
    ETX 4800,84
    GOTO 뉴전방하향20도
    GOTO RX_EXIT
    '***************

