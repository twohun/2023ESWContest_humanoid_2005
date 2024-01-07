# humanoid_embedded
## 프로젝트 소개
2023 임베디드소프트웨어 경진대회 지능형 휴머노이드 분야입니다. 이번 주제는 골프에서 파3, 파4 홀을 휴머노이드 로봇으로 성공하는 미션이였습니다.

<br/> 

## 팀원 소개
팀장 : 한양대 에리카 22학번 이진광

팀원 : 한양대 에리카 20학번 김지혁

팀원 : 한양대 에리카 20학번 이세훈

팀원 : 한양대 에리카 22학번 원두연

<br/> 

## 파3, 파4 영상
[![Video Label](http://img.youtube.com/vi/O7mWd3H0RnA/0.jpg)](https://youtu.be/O7mWd3H0RnA)

[![Video Label](http://img.youtube.com/vi/1el_z0uh7GU/0.jpg)](https://youtu.be/1el_z0uh7GU)

<br/> 

## 기본 행동 루프
<p align="center"><img src="/image/메인문.png" width="500"></p>

```py
while True:
        CAMERA.show_image()
        print('tasks_count : ', tasks_count)
        print('task_flag : ', const.TASK_FLAG)
        print('delay_count : ', delay_count)
        

        if const.TASK_FLAG == 1 and const.RCV_RX != 16 :
            if tasks_count == 0:
                #print('처음 공치는거')
                TX_data_py2(SERIAL, 33)
                const.NECK_POINTER = 1
                time.sleep(1)
                const.ROBOT_ANGLE = 30
                tasks_count = 1
                for i in range(10):
                    TX_data_py2(SERIAL, 41) #왼쪽으로 10
                    delay_time = 1000000
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                        CAMERA.show_image()
            #공 찾기
            elif tasks_count == 1:
                const.NECK_POINTER = 0
                sucess_t1 = find_ball.main()
                if sucess_t1:
                    tasks_count = 2
            #공 접근
            elif tasks_count == 2: 
                sucess_t2 = approch_ball.main()
                if sucess_t2:
                    tasks_count = 3
            #공 들어갔나 확인
            elif tasks_count == 3:
                sucess_t3 = check_finish.main()
                if sucess_t3:
                    tasks_count = 99  #끝!
                    delay_time = 1500000
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                        CAMERA.show_image()
                    TX_data_py2(SERIAL, 76)
                else:
                    delay_time = 1500000
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                        CAMERA.show_image()
                    delay_time = 500000
                    TX_data_py2(SERIAL, 73)
                    const.TASK_FLAG = 0
                    tasks_count = 4        
            # 동심원 돌기
            elif tasks_count == 4:
                sucess_t4 = rotate_robot.main()
                if sucess_t4:
                    tasks_count = 5
            # 홀 어레이 맞추기
            elif tasks_count == 5:
                sucess_t5 = array_shut.main()
                if sucess_t5:
                    tasks_count = 6
            elif tasks_count == 6:
                sucess_t6 = hit_turn.main()
                if sucess_t6:
                    tasks_count = 2
                else:
                    tasks_count = 1
       
        elif const.TASK_FLAG == 0 and const.RCV_RX != 16:
            if delay_count == 0:
                if(datetime.now()-const.NOW>timedelta(microseconds=const.DELAY_TIME)): #DELAY_TIME defalut is 500000
                    delay_count=1
                    const.DELAY_TIME = 500000 # 다시 딜레이 시간을 0.5s로
            elif delay_count == 1:
                print('finish delay')
                const.TASK_FLAG = 1
                delay_count = 0
        
        elif const.TASK_FLAG == 2:
            const.RCV_RX = 0
            tasks_count = 1
            approch_ball.clear_value()
            array_shut.clear_value  ()
```

메인문이다. 기본적으로 위의 사진과 같은 형태로 되어있다. 하지만 제어기에 제어 코드를 보내면 로봇이 움직이는 데, 시간이 걸린다. 이를 위해 microsecond 단위를 사용하여 스케쥴링 기법과 비슷하게, 시간을 나눠 카메라와 행동이 같이 움직일 수 있도록 하였다. 또한 넘어졌을 때를 판단하여, 넘어지면 일어날때 까지 기다렸다, 다시 공찾는 시퀀스로 무조건 되돌아가게 하여 다시 공을 찾고 접근하도록 코드를 구성하였다.

<br/> 

## 카메라 작업

다른 팀과 비슷한 cv작업을 했을 것이라 생각하고, 다른 점이라고 생각하는 점은 로봇의 pi카메라의 경우 카메라에 들어는 빛의 양에 따라 화이트 밸런스 같은 자동적으로 제어되는 기능들이 있다는 것을 확인 하였다. 이는 때에 따라서는 유용한 기능이였지만, 공을 찾거나 홀을 찾을 때, 화이트 밸런스가 순간적으로 변함에 따라 hsv값이 튀어 문제가 발생하였다. 따라서 picamer모듈을 이용하여 이를 직접 세팅하고 제어하였다.

```py
def set_image(self):
    self.camera = PiCamera()
    self.camera.resolution = (640, 480)
    self.camera.exposure_mode = 'off'
    self.camera.awb_mode = 'off' 
    # 경기장
    # self.camera.awb_gains = (Fraction(25, 16), Fraction(497, 256))

    # 케1
    self.camera.awb_gains = (Fraction(387, 256), Fraction(119, 64))
    self.cap = PiRGBArray(self.camera, size=(640, 480))
    time.sleep(0.1)
```

<br/> 

## 거리계산 알고리즘
### 수직 거리 계산
수직 거리 계산은 로봇으로 부터 얼만큼 떨어져 있는지를 계산한다.

<p align="center"><img src="/image/y계산1.png" width="300"></p>
<p align="center"><img src="/image/y계산2.png" width="300"></p>

```py
prop_A = (const.CAMERA_WIDTH - cY) / const.CAMERA_WIDTH #Y_value perspective proortion
distance_y = const.ROBOT_HEIGHT * math.tan(math.radians(const.ROBOT_ANGLE) - math.atan(-math.tan(math.radians(const.HEIGHT_FOV/2)*(2*prop_A - 1)))) #physical height distance of target
```
실제 사용한 코드에서는 prop_A에서 const.CAMERA_WIDTH가 쓰였다. 이는 const.CAMERA_HEIGHT로 고쳐야 한다.

### 수평 거리 계산
수평 거리 계산은 로봇의 중앙에서 수평으로 얼만큼 떨어져 있는지를 계산한다.

<p align="center"><img src="/image/x계산1.png" width="300"></p>
<p align="center"><img src="/image/x계산2.png" width="300"></p>
<p align="center"><img src="/image/x계산3.png" width="300"></p>
<p align="center"><img src="/image/x계산4.png" width="300"></p>

```py
prop_B = 0.5 + 1/(2 * math.tan(math.radians(const.HEIGHT_FOV/2)) * math.tan(math.radians(const.ROBOT_ANGLE))) # vanishing point of X_value perspective proportion
px_X = (prop_B * (const.CAMERA_WIDTH/2 - cX)) / (prop_B - 1 + cY/const.CAMERA_HEIGHT)
prop_X = - (2 * px_X) / const.CAMERA_WIDTH # vanishing point of X_vaqlue projection proportion
distance_x = (const.ROBOT_HEIGHT / math.cos(math.radians(const.ROBOT_ANGLE - const.HEIGHT_FOV/2))) * math.tan(math.radians(const.WIDTH_FOV/2)) * prop_X # physical height distance of target
```

### 홀 거리 보정
<p align="center"><img src="/image/화각보정1.png" width="300"></p>
퍼팅하기 위한 자리에 위치하려는 경우,수평 거리를 많이 사용하게 된다. 우리의 알고리즘상 위의 사진과 같은 형태가 나오게 된다. 이런 상황에서는 왼쪽 화면은 쓰지 않게 된다. 따라서 수평화각의 절반(로봇기준으로 90도 - 수평화각/2)만큼 오른쪽으로 돌려 이를 막았다.
<p align="center"><img src="/image/화각보정2.png" width="300"></p>
고개를 돌리므로써 거리 값에 오차가 생겼으므로 보정을 해야 한다. 우리가 구해야 하는 것은 위의 그림에서 dist_x의 값이다. 구할수 있는 값은 x와 x'이므로 이를 통해 dist_x'을 추정하고 theta가 닮음에 의하여 수평화각의 절반이므로 삼각비를 통하여 dist_x값을 구하였다.

```py
prop_B = 0.5 + 1/(2 * math.tan(math.radians(const.HEIGHT_FOV/2)) * math.tan(math.radians(const.ROBOT_ANGLE))) # vanishing point of X_value perspective proportion
px_X = (prop_B * (const.CAMERA_WIDTH/2 - cX)) / (prop_B - 1 + cY/const.CAMERA_HEIGHT)
prop_X = - (2 * px_X) / const.CAMERA_WIDTH # vanishing point of X_vaqlue projection proportion
distance_ax = (const.ROBOT_HEIGHT / math.cos(math.radians(const.ROBOT_ANGLE - const.HEIGHT_FOV/2))) * math.tan(math.radians(const.WIDTH_FOV/2)) * prop_X
px_wX = (prop_B * (const.CAMERA_WIDTH/2)) / (prop_B - 1 + cY/const.CAMERA_HEIGHT)
prop_wX = - (2 * px_wX) / const.CAMERA_WIDTH
distance_wx = abs((const.ROBOT_HEIGHT / math.cos(math.radians(const.ROBOT_ANGLE - const.HEIGHT_FOV/2))) * math.tan(math.radians(const.WIDTH_FOV/2)) * prop_wX)
distance_x = math.cos(math.radians(12.14))*(distance_wx + distance_ax)
```
