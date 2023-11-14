
from __init__ import *
from Serial_python3_1 import *
from datetime import timedelta, datetime


def control_trackbar():
    #threading
    cv2.namedWindow("Trackbar Windows", flags=cv2.WINDOW_NORMAL)
    cv2.createTrackbar("max_H", "Trackbar Windows", 0, 255, lambda x : x)
    cv2.createTrackbar("min_H", "Trackbar Windows", 0, 255, lambda x : x)
    cv2.createTrackbar("max_S", "Trackbar Windows", 0, 255, lambda x : x)
    cv2.createTrackbar("min_S", "Trackbar Windows", 0, 255, lambda x : x)
    cv2.createTrackbar("max_V", "Trackbar Windows", 0, 255, lambda x : x)
    cv2.createTrackbar("min_V", "Trackbar Windows", 0, 255, lambda x : x)
    cv2.createTrackbar("min_Va", "Trackbar Windows", 0, 255, lambda x : x)

    cv2.setTrackbarPos("max_H", "Trackbar Windows", 185)
    cv2.setTrackbarPos("min_H", "Trackbar Windows", 138)
    cv2.setTrackbarPos("max_S", "Trackbar Windows", 253)
    cv2.setTrackbarPos("min_S", "Trackbar Windows", 100)
    cv2.setTrackbarPos("max_V", "Trackbar Windows", 255)
    cv2.setTrackbarPos("min_V", "Trackbar Windows", 44)
    cv2.setTrackbarPos("min_Va", "Trackbar Windows", 255)

def open_camera():
    global camera
    camera = cv2.VideoCapture(0)
    print("원래 가로 : {}, 높이 : {}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))) 
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, X) # 가로
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,Y) # 세로
    #control_trackbar()
    print(str(V_angle))

def Camera_distance_ball():
    cX = cY = distance_x = distance_y = L1_norm = 0
    # global cX, cY, distance_x, distance_y, L1_norm
    (grabbed, frame) = camera.read()
    # print("원래 가로 : {}, 높이 : {}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if grabbed:
        cv2.circle(frame, (int(X/2), int(Y/2)), 5, (255, 255, 255), -1)
        Mh = 179 #cv2.getTrackbarPos("max_H", "Trackbar Windows")
        mh = 63 #cv2.getTrackbarPos("min_H", "Trackbar Windows")
        Ms = 255 #cv2.getTrackbarPos("max_S", "Trackbar Windows")
        ms = 79 #cv2.getTrackbarPos("min_S", "Trackbar Windows")
        Mv = 255 #cv2.getTrackbarPos("max_V", "Trackbar Windows")
        mv = 145  #cv2.getTrackbarPos("min_V", "Trackbar Windows")
        
        lower = np.array([mh, ms, mv], dtype = "uint8")
        upper = np.array([Mh, Ms, Mv], dtype = "uint8")
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #lower = np.array([0, 0, 235], dtype = "uint8")
            #upper = np.array([50, 50, 255], dtype = "uint8")
        Masked = cv2.inRange(converted, lower, upper)
        Mask = cv2.GaussianBlur(Masked, (3, 3), 0)
        contours, _ = cv2.findContours(Mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        maxArea = 0
        max_id = 0
        count = 0
        
        # cv2.imshow('visual', frame)
        # cv2.imshow('befo', Masked)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > maxArea:
                maxArea = area
                max_id = count
            count += 1

        if max_id == len(contours):
            #print("not detect")
            return cX, cY, distance_x, distance_y, L1_norm
        if maxArea < 800 :
            return cX, cY, distance_x, distance_y, L1_norm
            
        ball_contour = contours[max_id]     
        moment = cv2.moments(ball_contour)
           
        # calculate x,y coordinate of centerq
        cX = int(moment['m10'] / moment['m00'])
        cY = int(moment['m01'] / moment['m00'])             
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        ######calc######
        prop_A = (X - cY) / X #Y_value perspective proportion
        prop_B = 0.5 + 1/(2 * tan(radians(H_angle/2)) * tan(radians(V_angle))) # vanishing point of X_value perspective proportion
        px_X = (prop_B * (X/2 - cX)) / (prop_B - 1 + cY/Y)
        prop_X = - (2 * px_X) / X # vanishing point of X_vaqlue projection proportion
        #prop_X = prop_X * 1.031 # calibration
        distance_y = Robot_height * tan(radians(V_angle) - atan(-tan(radians(H_angle/2)*(2*prop_A - 1)))) #physical height distance of target
        distance_x = (Robot_height / cos(radians(V_angle - H_angle/2))) * tan(radians(W_angle/2)) * prop_X # physical height distance of target
        L1_norm = sqrt(np.square(distance_x) + np.square(distance_y))
        ####calc_end####
        cv2.putText(frame, "centroid : " + str(cX) + ", " + str(cY) , (10 ,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, "Y : " + str(distance_y), (10, 23),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, "X : " + str(distance_x), (10, 36),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, "L : " + str(L1_norm), (10, 49),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.drawContours(frame, contours, 0, [0,255,0])
                     
            # show the image
        #v2.imshow('befo', Masked)
        #cv2.drawContours(frame, line[1], -1, (255,255,255), 3
        print('cx',cX, ' cy',cY)
    return cX, cY, distance_x, distance_y, L1_norm 
    
def Camera_distance_hole():
    a_x = a_y = dist_ax = dist_ay = dist_al = 0
    # global cX, cY, distance_x, distance_y, L1_norm
    (grabbed, frame) = camera.read()
    # print("원래 가로 : {}, 높이 : {}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if grabbed:
        cv2.circle(frame, (int(X/2), int(Y/2)), 5, (255, 255, 255), -1)
        Mh = 179 #cv2.getTrackbarPos("max_H", "Trackbar Windows")
        mh = 63 #cv2.getTrackbarPos("min_H", "Trackbar Windows")
        Ms = 255 #cv2.getTrackbarPos("max_S", "Trackbar Windows")
        ms = 79 #cv2.getTrackbarPos("min_S", "Trackbar Windows")
        Mv = 255 #cv2.getTrackbarPos("max_V", "Trackbar Windows")
        mv = 145  #cv2.getTrackbarPos("min_V", "Trackbar Windows")
           
        lower = np.array([mh, ms, mv], dtype = "uint8")
        upper = np.array([Mh, Ms, Mv], dtype = "uint8")
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
           #lower = np.array([0, 0, 235], dtype = "uint8")
           #upper = np.array([50, 50, 255], dtype = "uint8")
        Masked = cv2.inRange(converted, lower, upper)
        Mask = cv2.GaussianBlur(Masked, (3, 3), 0)
        contours, _ = cv2.findContours(Mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        max = 0 
        if len(contours) != 0 :
            index = 0
            for i in range(len(contours[:4])):
                M = cv2.moments(contours[i])
                if M["m00"] != 0:              
                     # calculate x,y coordinate of centerq
                    
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                        ######calc######
                
                    a_x, a_y, dist_ax, dist_ay, dist_al = dist_cal(cX, cY)
                    w_x, w_y, dist_wx, dist_wy, dist_wl = dist_cal(0, cY)
                    distance_x = dist_wx - dist_ax
                    
                    
                         ####calc_end####
                    cv2.putText(frame, "centroid : " + str(cX) + ", " + str(cY) , (10 ,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    #cv2.putText(frame, "Y : " + str(distance_y), (10, 23),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.putText(frame, "X : " + str(distance_x), (10, 36),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    #cv2.putText(frame, "L : " + str(L1_norm), (10, 49),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.drawContours(frame, contours, 0, [0,255,0])
                     
            # show the image
        cv2.imshow('befo', Masked)
        cv2.imshow('mask', Mask)
        #cv2.drawContours(frame, line[1], -1, (255,255,255), 3)
        cv2.imshow('visual', frame)
    return cX, cY, distance_x, dist_ay, dist_al

def Camera_distance_hole2():
    cX = cY = distance_x = distance_y = L1_norm = 0
    # global cX, cY, distance_x, distance_y, L1_norm
    (grabbed, frame) = camera.read()
    # print("원래 가로 : {}, 높이 : {}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if grabbed:
        cv2.circle(frame, (int(X/2), int(Y/2)), 5, (255, 255, 255), -1)
        Mh = 36 #cv2.getTrackbarPos("max_H", "Trackbar Windows")
        mh = 21 #cv2.getTrackbarPos("min_H", "Trackbar Windows")
        Ms = 171 #cv2.getTrackbarPos("max_S", "Trackbar Windows")
        ms = 44 #cv2.getTrackbarPos("min_S", "Trackbar Windows")
        Mv = 255 #cv2.getTrackbarPos("max_V", "Trackbar Windows")
        mv = 221  #cv2.getTrackbarPos("min_V", "Trackbar Windows")
            
        lower = np.array([mh, ms, mv], dtype = "uint8")
        upper = np.array([Mh, Ms, Mv], dtype = "uint8")
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #lower = np.array([0, 0, 235], dtype = "uint8")
            #upper = np.array([50, 50, 255], dtype = "uint8")
        Masked = cv2.inRange(converted, lower, upper)
        Mask = cv2.GaussianBlur(Masked, (3, 3), 0)
        contours, _ = cv2.findContours(Mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        maxArea = 0
        max_id = 0
        count = 0
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > maxArea:
                maxArea = area
                max_id = count
            count += 1

        if max_id == len(contours):
            print("not detect")
            return cX, cY, distance_x, distance_y, L1_norm
        if maxArea < 800 :
            return cX, cY, distance_x, distance_y, L1_norm
            
        hole_contour = contours[max_id]     
        moment = cv2.moments(hole_contour)
           
        # calculate x,y coordinate of centerq
        cX = int(moment['m10'] / moment['m00'])
        cY = int(moment['m01'] / moment['m00'])             
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        ######calc######
        prop_A = (X - cY) / X #Y_value perspective proportion
        prop_B = 0.5 + 1/(2 * tan(radians(H_angle/2)) * tan(radians(V_angle))) # vanishing point of X_value perspective proportion
        px_X = (prop_B * (X/2 - cX)) / (prop_B - 1 + cY/Y)
        prop_X = - (2 * px_X) / X # vanishing point of X_vaqlue projection proportion
        distance_ax = (Robot_height / cos(radians(V_angle - H_angle/2))) * tan(radians(W_angle/2)) * prop_X
        px_wX = (prop_B * (X/2)) / (prop_B - 1 + cY/Y)
        prop_wX = - (2 * px_wX) / X
        distance_wx = (Robot_height / cos(radians(V_angle - H_angle/2))) * tan(radians(W_angle/2)) * prop_wX
        #prop_X = prop_X * 1.031 # calibration
        distance_y = Robot_height * tan(radians(V_angle) - atan(-tan(radians(H_angle/2)*(2*prop_A - 1)))) #physical height distance of target
        distance_x = distance_ax - distance_wx #(Robot_height / cos(radians(V_angle - H_angle/2))) * tan(radians(W_angle/2)) * prop_X # physical height distance of target
        L1_norm = sqrt(np.square(distance_x) + np.square(distance_y))

        
        ####calc_end####
        cv2.putText(frame, "centroid : " + str(cX) + ", " + str(cY) , (10 ,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, "Y : " + str(distance_y), (10, 23),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, "X : " + str(distance_x), (10, 36),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, "L : " + str(L1_norm), (10, 49),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.drawContours(frame, contours, 0, [0,255,0])
                     
            # show the image
        #cv2.imshow('befo', Masked)
        #cv2.imshow('hole_mask', Mask)
        #cv2.drawContours(frame, line[1], -1, (255,255,255), 3)
        #cv2.imshow('visual', frame)
        print('hole cx {0} hole cy{1} hole dist_x{2}'.format(cX, cY, distance_x))
        
        return cX, cY, distance_x, distance_y, L1_norm
    else:
        cX = cY = distance_x = distance_y = L1_norm = 1
        return cX, cY, distance_x, distance_y, L1_norm

def dist_cal(pixel_x, pixel_y):
    cX = cY = distance_x = distance_y = L1_norm = 0
    cX = pixel_x
    cY = pixel_y
    prop_A = (X - pixel_y) / X #Y_value perspective proportion
    prop_B = 0.5 + 1/(2 * tan(radians(H_angle/2)) * tan(radians(V_angle))) # vanishing point of X_value perspective proportion
    px_X = (prop_B * (X/2 - pixel_x)) / (prop_B - 1 + pixel_y/Y)
    prop_X = - (2 * px_X) / X # vanishing point of X_vaqlue projection proportion
       #prop_X = prop_X * 1.031 # calibration
    distance_y = Robot_height * tan(radians(V_angle) - atan(-tan(radians(H_angle/2)*(2*prop_A - 1)))) #physical height distance of target
    distance_x = (Robot_height / cos(radians(V_angle - H_angle/2))) * tan(radians(W_angle/2)) * prop_X # physical height distance of target
    L1_norm = sqrt(np.square(distance_x) + np.square(distance_y))
    return cX, cY, distance_x, distance_y, L1_norm

def set_serial():
    BPS = 4800
    serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
    serial_port.flush()
    return serial_port

def set_ball_center(x):
    if int(x)>360:
        #set_serial()
        #serial_port.write(serial.to_bytes([9]))
        TX_data_py2(serial_port, 69) #Right turn 5
    elif int(x)<280 and x!=0 :
        TX_data_py2(serial_port, 67) #Left turn 5
        
def set_ball_center2(x):
    if int(x)>360:
        #set_serial()
        #serial_port.write(serial.to_bytes([9]))
        TX_data_py2(serial_port, 42) #Right turn 5
    elif int(x)<280 and x!=0 :
        TX_data_py2(serial_port, 41) #Left turn 5

def set_ball_hit(x):
    if int(x)>490:
        #set_serial()
        #serial_port.write(serial.to_bytes([9]))
        TX_data_py2(serial_port, 42) #Right sidestep 10
    elif int(x)<410 and x!=0 :
        TX_data_py2(serial_port, 41) #Left sidestep 10

def set_hole_hit(x):
    if float(x)>17: #실제 거리 기준으로는 17
        #set_serial()
        #serial_port.write(serial.to_bytes([9]))
        TX_data_py2(serial_port, 69) #Right turn 5
    elif float(x)<15 and x!=0 : #여기도 15
        TX_data_py2(serial_port, 67) #Left turn 5

def find_hole(x):
    if float(x)==0:
        TX_data_py2(serial_port, 43)
        

def get_point():
    if rl_head_cnt == 0:
        pixel_x, pixel_y, real_dist_x, real_dist_y, real_dist_l = Camera_distance_ball() #센터 맞추기
        return  pixel_x, pixel_y, real_dist_x, real_dist_y, real_dist_l
    elif rl_head_cnt == 90:
        pixel_x, pixel_y, real_dist_x, real_dist_y, real_dist_l = Camera_distance_hole()
        return pixel_x, pixel_y, real_dist_x, real_dist_y, real_dist_l



    
def find_ball():
    iter=46
    set_num=0
    rotate_fun=0
    TX_data_py2(serial_port,39)
    time.sleep(0.5)
    TX_data_py2(serial_port,iter)
    time.sleep(1)
    while True:
        print('ITER', iter)
        c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
        if set_num==0:
            if iter > 55:
                
                break
            if abs(c_x-320) < 150:
                TX_data_py2(serial_port,23)
                time.sleep(0.1)
                TX_data_py2(serial_port,55)
                rotate=55-iter  
                set_num=2
            else:
                set_num=1
                pre_num=0
                TX_data_py2(serial_port,iter)
                iter=iter+1
                now=datetime.now()
        elif set_num==2: # rotate function
            print('ROTATE', rotate)
            if rotate_fun <= rotate:
                TX_data_py2(serial_port,70)
                set_num=3
                pre_num=2
                rotate_fun=rotate_fun + 1 #원래 rotate_fun + 1인데 너무 많이돌아서 바꿈
                now=datetime.now()
            else:
                return True

        elif set_num==1: # timer function
            if(datetime.now()-now>timedelta(microseconds=300000)):
                set_num=pre_num
        elif set_num==3: # timer function
            if(datetime.now()-now>timedelta(microseconds=1000000)):
                set_num=pre_num
        if cv2.waitKey(1) != -1:
            break
    
    TX_data_py2(serial_port,60)
    time.sleep(0.5)
    iter = 60
    set_num = 0
    rotate_fun=0
    TX_data_py2(serial_port,iter)
    time.sleep(1)

    while True:
        c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
        if set_num==0:
            if iter < 55:
                break
            if abs(c_x-320) < 150:
                TX_data_py2(serial_port,23)
                time.sleep(0.1)
                TX_data_py2(serial_port,55)
                rotate=iter-55
                set_num=2
            else:
                set_num=1
                pre_num=0
                TX_data_py2(serial_port,iter)
                iter=iter-1
                now=datetime.now()
        elif set_num==2: # rotate function
            print(rotate)
            if rotate_fun <= rotate:
                TX_data_py2(serial_port,72  )
                set_num=3
                pre_num=2
                rotate_fun=rotate_fun + 1
                now=datetime.now()
            else:
                return True

        elif set_num==1: # timer function
            if(datetime.now()-now>timedelta(microseconds=300000)):
                set_num=pre_num
        elif set_num==3: # timer function
            if(datetime.now()-now>timedelta(microseconds=1000000)):
                set_num=pre_num
        if cv2.waitKey(1) != -1:
            break
    return False

neck_list = [39, 33, 37, 34, 31, 36, 29] # 순서대로 20도, 30도, 40도, 50도, 60도, 70도, 80도
neck_value = [20,30, 40,50, 60,70, 80]
neck_pointer = 0
set_num_2_cnt = 0
set_num_3_cnt = 0
set_num_4_cnt = 0
set_num_5_cnt = 0
doesnt_find=0
find_hole_cnt=0
set_cnt = 0
head_cnt = 60
rl_head_cnt = 0
start_num = 0
main_num = 0 
pre_num = 0
set_num = 6
calibration_count = 0
shut_cout = 0
find_iter = 0 #홀 찾을 때 움직이고 기다릴 때 사용되는 변수
array_count = 0
a = 0
if __name__ == "__main__":
    now=datetime.now()
    open_camera()
    serial_port = set_serial()
    TX_data_py2(serial_port, 31)
    time.sleep(1.5)
    while True:
        #print('nect_point', neck_pointer)
        print('set_num : ', set_num)
        print('set_num_2_cnt : ', set_num_2_cnt)
        print('set_num_3_cnt : ', set_num_3_cnt)
        print('set_num_4_cnt : ', set_num_4_cnt)
        print('set_num_5_cnt : ', set_num_5_cnt)

        if set_num == 1: # 공 찾기 
            for i in range(len(neck_list)):
                TX_data_py2(serial_port, neck_list[neck_pointer])
                time.sleep(0.5)
                success = find_ball()
                if success:
                    head_cnt = neck_value[neck_pointer]
                    neck_pointer = 0
                    set_num = 2
                    break
                neck_pointer = (neck_pointer + 1) % 7
        elif set_num == 2: # 공 어프로치
            c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
            if set_num_2_cnt == 0:
                neck_pointer = int((head_cnt)/10 - 2)
                set_num_2_cnt = 1
            elif set_num_2_cnt == 1:
                if int(c_x) < 280 or int(c_x) > 360:
                    set_ball_center(c_x)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                else:
                    set_num_2_cnt = 2

            elif set_num_2_cnt == 2:
                if int(c_y) < 300 and int(c_y) > 0:
                    TX_data_py2(serial_port, 11)
                    time.sleep(0.1)
                    TX_data_py2(serial_port,23)
                    time.sleep(1)
                    set_num_2_cnt = 1
                elif int(c_y) >= 300:
                    if neck_pointer <= 2:
                        set_num_2_cnt = 0
                        set_num = 3
                        TX_data_py2(serial_port, 73) #81도 돌기
                        time.sleep(1)
                        TX_data_py2(serial_port, 73) #81도 돌기
                        time.sleep(1)
                        TX_data_py2(serial_port, 73) #81도 돌기
                        time.sleep(1)
                        head_cnt = neck_value[neck_pointer]
                        V_angle = head_cnt
                        continue

                    neck_pointer = neck_pointer - 1
                    time.sleep(1)
                    TX_data_py2(serial_port,neck_list[neck_pointer])
                    time.sleep(1)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                    set_num_2_cnt = 1
                else: 
                    set_num = 1
                    set_num_2_cnt =0
                    neck_pointer = 0
            elif set_num_2_cnt == 3:
                pass
                    

        elif set_num == 3: # 공 들어갔는지 판단
           # b_x, b_y, dist_bx, dist_by, dist_bl = Camera_distance_ball()
           # h_x, h_y, dist_hx, dist_hy, dist_hl = Camera_distance_hole()
           # if abs(b_x-h_x) < 20 and abs(b_y-h_y):
           #     print('done')
           # else:
            set_num = 4
        elif set_num == 4: # 홀 찾기
            head_val = [80, 60, 40]
            head_lis = [78, 80, 82]
            if set_num_4_cnt == 0:
                #여기서 머리 위아래 / 머리 위아래로 작동 시키로 0번으로 와서 찍고 옮기고 하는 방식으로 생각하기
                for i in range(0,3) : # 20 40 60
                    time.sleep(0.5)
                    TX_data_py2(serial_port, head_lis[i])
                    time.sleep(2)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole2()
                    
                    if (c_x != 0 or c_y != 0): # 인식하면
                        print("detected, now : ", head_val[i-1])
                        TX_data_py2(serial_port, head_lis[i-1])
                        head_cnt = head_val[i-1]
                        V_angle = head_cnt
                        calibration_count=0
                        set_num = 5 # set_num 5에서의 홀 맞추기로 보내기
                        set_num_5_cnt = 0
                        a = i - 1
                        break
                    elif c_x == 0 and c_y == 0: #else: 
                        set_num_4_cnt = 1
                
            elif set_num_4_cnt == 1: # 동심원 도는 부분
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole2()#None, None, None, None, None
                #print("coiunt_43 : " + str(count_43))
                rx_num = RX_data(serial_port)
                TX_data_py2(serial_port, 43)
                time.sleep(4)
                set_num_4_cnt = 0

        elif set_num == 5: # 퍼팅 보정
            if set_num_5_cnt == 0:
                print('a')
                time.sleep(1)
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole2()
                print("c_x : ", c_x, " c_y : ", c_y, " dist_x : ", dist_x)
                if int(dist_x)!=0:
                    print('b')
                    #find_iter = 0
                    set_hole_hit(dist_x)
                    time.sleep(1)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole2()
                    if float(dist_x) <= 17.0 and float(dist_x) >= 15.0 and calibration_count < 1:
                        TX_data_py2(serial_port, 39) #머리 전방 20도 내리기
                        time.sleep(2)
                        set_num_5_cnt = 1 #여기는 발 밑 공 세팅 
                        calibration_count += 1
                    elif float(dist_x) <= 17.0 and float(dist_x) >= 15.0 and calibration_count > 0: #고개 내릴 때 calibration_count 올라감
                        set_num = 6 # 6번에서 이에 대한 판단으로 마지막 판단할 것'
                '''
                elif int(dist_x) == 0:
                    set_num = 4
                    set_num_4_cnt = 0
                '''
            if set_num_5_cnt == 1:   # 지금 여기서 볼 좌우 안맞춤
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                if array_count == 0:
                    if c_y <= 380 and c_y >=280:
                        array_count = 1
                    elif c_y >380:
                        TX_data_py2(serial_port, 12)
                        TX_data_py2(serial_port,23)
                        time.sleep(1)
                    elif c_y <280:
                        TX_data_py2(serial_port, 32)
                        TX_data_py2(serial_port,23)
                        time.sleep(1)
                elif array_count == 1:
                    set_ball_hit(c_x)
                    time.sleep(1)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                    if c_x <= 490 or c_x >=410 :
                        set_num_3_cnt = 4
                        TX_data_py2(serial_port, 73) 
                        time.sleep(1)
                        TX_data_py2(serial_port, head_lis[a])
                        time.sleep(1)
                        array_count = 0
                '''
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                set_ball_hit(c_x)
                if c_x <= 490 or c_x >=410 :
                    set_num_5_cnt = 0
                 