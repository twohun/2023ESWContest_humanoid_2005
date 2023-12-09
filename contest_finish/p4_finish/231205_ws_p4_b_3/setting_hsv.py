import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

mx, my = 0, 0 
camera_width = 480
camera_height = 640
def mouse_move( event,x,y,flags,param):
  global mx, my
  if event == cv2.EVENT_MOUSEMOVE:
    mx, my = x, y

def draw_str2(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255), lineType=cv2.LINE_AA)

def nothing(x):
    pass

camera = PiCamera()
camera.resolution = (camera_height, camera_width)
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = (387/256, 477/256)

cap = PiRGBArray(camera, size=(camera_height, camera_width))
time.sleep(0.1)

# 창 생성
cv2.namedWindow('Track')

# 트랙바 생성
cv2.createTrackbar('Hue Min', 'Track', 0, 255, nothing)
cv2.createTrackbar('Hue Max', 'Track', 255, 255, nothing)
cv2.createTrackbar('Saturation Min', 'Track', 0, 255, nothing)
cv2.createTrackbar('Saturation Max', 'Track', 255, 255, nothing)
cv2.createTrackbar('Value Min', 'Track', 0, 255, nothing)
cv2.createTrackbar('Value Max', 'Track', 255, 255, nothing)

while True:
    # 트랙바 값 가져오기
    hue_min = cv2.getTrackbarPos('Hue Min', 'Track')
    hue_max = cv2.getTrackbarPos('Hue Max', 'Track')
    saturation_min = cv2.getTrackbarPos('Saturation Min', 'Track')
    saturation_max = cv2.getTrackbarPos('Saturation Max', 'Track')
    value_min = cv2.getTrackbarPos('Value Min', 'Track')
    value_max = cv2.getTrackbarPos('Value Max', 'Track')
    camera.capture(cap, format="bgr", use_video_port=True)
    image = cap.array
    cap.truncate(0)

    # HSV로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 범위 설정
    lower_range = np.array([hue_min, saturation_min, value_min])
    upper_range = np.array([hue_max, saturation_max, value_max])

    # 마스크 생성
    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.GaussianBlur(mask, (9,9), 0)
    mx2 = mx
    my2 = my

    if mx2 < camera_width and my2 < camera_height:
      pixel = hsv[my2, mx2]
      set_H = pixel[0]
      set_S = pixel[1]
      set_V = pixel[2]

      
      x_p = 30
      draw_str2(image, (mx2 - x_p, my2 + 15), '-HSV-')
      draw_str2(image, (mx2 - x_p, my2 + 30), '%.1d' % (set_H))
      draw_str2(image, (mx2 - x_p, my2 + 45), '%.1d' % (set_S))
      draw_str2(image, (mx2 - x_p, my2 + 60), '%.1d' % (set_V))

    # 창에 이미지 표시
    cv2.imshow('Image',image)
    cv2.setMouseCallback('Image', mouse_move)
    cv2.imshow('Mask', mask)
    print('awb :',camera.awb_gains)
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 창 닫기
cv2.destroyAllWindows()
