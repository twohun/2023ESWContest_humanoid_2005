# humanoid_embedded
## 프로젝트 소개
2023 임베디드소프트웨어 경진대회 지능형 휴머노이드 분야입니다. 이번 주제는 골프에서 파3, 파4 홀을 휴머노이드 로봇으로 성공하는 미션이였습니다.

## 팀원 소개
팀장 : 한양대 에리카 22학번 이진광

팀원 : 한양대 에리카 20학번 김지혁

팀원 : 한양대 에리카 20학번 이세훈

팀원 : 한양대 에리카 22학번 원두연

## 파3, 파4 영상
[![Video Label](http://img.youtube.com/vi/O7mWd3H0RnA/0.jpg)](https://youtu.be/O7mWd3H0RnA)

[![Video Label](http://img.youtube.com/vi/1el_z0uh7GU/0.jpg)](https://youtu.be/1el_z0uh7GU)

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
