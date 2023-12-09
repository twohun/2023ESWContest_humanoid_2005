import cv2
import numpy as np
import math
import constant_value as const
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from fractions import Fraction
class INIT_CV():
    def __init__(self):
        
        self.set_image()
        # set mask
        self.yello_hsv = const.YELLO_MASK
        '''
        yello hsv info [[lower], [upper] ]
        '''
        self.red_hsv = const.RED_MASK
        '''
        red hsv info [[lower], [upper]]
        '''

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

    def get_image(self):
        self.camera.capture(self.cap, format="bgr", use_video_port=True)
        image = self.cap.array
        self.cap.truncate(0)
        return image

    def get_hsv_image(self):
        hsv_image = cv2.cvtColor(self.get_image(), cv2.COLOR_BGR2HSV)
        return hsv_image  
      
    def get_mask(self, lower, upper):
        '''
        lower is hsv lower value list\n
        upper is hsv upper value list 
        '''
        hsv_lower = np.array(lower, dtype="uint8" )
        hsv_upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(self.get_hsv_image(), hsv_lower, hsv_upper)
        gausisian_mask = cv2.GaussianBlur(mask, (3, 3), 0)
        return gausisian_mask
    
    def show_image(self):
        '''
        only show image use to imshow
        '''
        image = self.get_image()
        yello_mask = self.get_mask(self.yello_hsv[0], self.yello_hsv[1])
        red_mask = self.get_mask(self.red_hsv[0], self.red_hsv[1])

        cv2.imshow('row_image',image)
        cv2.imshow('yello_mask', yello_mask)
        cv2.imshow('red_mask', red_mask)
        cv2.waitKey(1) #camera가 갱신될때 까지 어느정도 기다림 1000ms = 1s

    def get_info_ball(self):
        cX = cY = distance_x = distance_y = L1_norm = 0
        mask = self.get_mask(self.red_hsv[0],self.red_hsv[1])
        mask = cv2.GaussianBlur(mask, (7,7), 0)
        contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
   
        max_area = 0
        max_id = 0
        count = 0
        #check largest contour
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_id = count
            count += 1

        # check threshold
        if max_id == len(contours):
            print("not ball detect")
            return cX, cY, distance_x, distance_y, L1_norm
        if max_area < 100 :
            print("not ball over area")
            return cX, cY, distance_x, distance_y, L1_norm
        
        ball_contour = contours[max_id]     
        moment = cv2.moments(ball_contour)

        # calculate x,y coordinate of centerq
        cX = int(moment['m10'] / moment['m00'])
        cY = int(moment['m01'] / moment['m00']) 
        
        prop_A = (const.CAMERA_WIDTH - cY) / const.CAMERA_WIDTH #Y_value perspective proportion
        prop_B = 0.5 + 1/(2 * math.tan(math.radians(const.HEIGHT_FOV/2)) * math.tan(math.radians(const.ROBOT_ANGLE))) # vanishing point of X_value perspective proportion
        px_X = (prop_B * (const.CAMERA_WIDTH/2 - cX)) / (prop_B - 1 + cY/const.CAMERA_HEIGHT)
        prop_X = - (2 * px_X) / const.CAMERA_WIDTH # vanishing point of X_vaqlue projection proportion

        distance_y = const.ROBOT_HEIGHT * math.tan(math.radians(const.ROBOT_ANGLE) - math.atan(-math.tan(math.radians(const.HEIGHT_FOV/2)*(2*prop_A - 1)))) #physical height distance of target
        distance_x = (const.ROBOT_HEIGHT / math.cos(math.radians(const.ROBOT_ANGLE - const.HEIGHT_FOV/2))) * math.tan(math.radians(const.WIDTH_FOV/2)) * prop_X # physical height distance of target
        L1_norm = math.sqrt(np.square(distance_x) + np.square(distance_y))

        print(f'get ball cx : {cX}, cy : {cY}, area : {max_area}')

        return cX, cY, distance_x, distance_y, L1_norm
    
    def get_info_hole(self):
        cX = cY = distance_x = distance_y = L1_norm = 0
        mask = self.get_mask(self.yello_hsv[0],self.yello_hsv[1])
        mask = cv2.GaussianBlur(mask, (9,9), 0)
        contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        max_area = 0
        max_id = 0
        count = 0
        #check largest contour
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                max_id = count
            count += 1

        # check threshold
        if max_id == len(contours):
            print("not hole detect")
            return cX, cY, distance_x, distance_y, L1_norm
        if max_area  < 100 :
            print("not hole over area")
            return cX, cY, distance_x, distance_y, L1_norm
        
        hole_contour = contours[max_id]     
        moment = cv2.moments(hole_contour)
        # calculate x,y coordinate of centerq
        cX = int(moment['m10'] / moment['m00'])
        cY = int(moment['m01'] / moment['m00'])  

        prop_A = (const.CAMERA_WIDTH - cY) / const.CAMERA_WIDTH #Y_value perspective proportion
        prop_B = 0.5 + 1/(2 * math.tan(math.radians(const.HEIGHT_FOV/2)) * math.tan(math.radians(const.ROBOT_ANGLE))) # vanishing point of X_value perspective proportion
        px_X = (prop_B * (const.CAMERA_WIDTH/2 - cX)) / (prop_B - 1 + cY/const.CAMERA_HEIGHT)
        prop_X = - (2 * px_X) / const.CAMERA_WIDTH # vanishing point of X_vaqlue projection proportion
        distance_ax = (const.ROBOT_HEIGHT / math.cos(math.radians(const.ROBOT_ANGLE - const.HEIGHT_FOV/2))) * math.tan(math.radians(const.WIDTH_FOV/2)) * prop_X
        px_wX = (prop_B * (const.CAMERA_WIDTH/2)) / (prop_B - 1 + cY/const.CAMERA_HEIGHT)
        prop_wX = - (2 * px_wX) / const.CAMERA_WIDTH
        distance_wx = abs((const.ROBOT_HEIGHT / math.cos(math.radians(const.ROBOT_ANGLE - const.HEIGHT_FOV/2))) * math.tan(math.radians(const.WIDTH_FOV/2)) * prop_wX)
        #prop_X = prop_X * 1.031 # calibration
        
        distance_y = const.ROBOT_HEIGHT * math.tan(math.radians(const.ROBOT_ANGLE) - math.atan(-math.tan(math.radians(const.HEIGHT_FOV/2)*(2*prop_A - 1)))) #physical height distance of target
        distance_x = math.cos(math.radians(12.14))*(distance_wx + distance_ax) #(Robot_height / cos(radians(V_angle - H_angle/2))) * tan(radians(W_angle/2)) * prop_X # physical height distance of target
        L1_norm = math.sqrt(np.square(distance_x) + np.square(distance_y))
        
        print(f'get hole cx : {cX}, cy : {cY}, dist_ax : {distance_ax}, dist_wx : {distance_wx}, dist_x : {distance_x}')
        return cX, cY, distance_x, distance_y, L1_norm
    
