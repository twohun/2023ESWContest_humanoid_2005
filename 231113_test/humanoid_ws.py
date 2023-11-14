from __init__ import *
from Serial_python3_1 import *
import time
set_num = 0

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
    control_trackbar()
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
         cv2.imshow('befo', Masked)
         cv2.imshow('mask', Mask)
         #cv2.drawContours(frame, line[1], -1, (255,255,255), 3)
         cv2.imshow('visual', frame)
    return cX, cY, distance_x, distance_y, L1_norm 
   
def Camera_distance_hole():
    cX = cY = distance_x = distance_y = L1_norm = 0
    # global cX, cY, distance_x, distance_y, L1_norm
    (grabbed, frame) = camera.read()
    # print("원래 가로 : {}, 높이 : {}".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if grabbed:
         cv2.circle(frame, (int(X/2), int(Y/2)), 5, (255, 255, 255), -1)
         Mh = 43 #cv2.getTrackbarPos("max_H", "Trackbar Windows")
         mh = 0 #cv2.getTrackbarPos("min_H", "Trackbar Windows")
         Ms = 255 #cv2.getTrackbarPos("max_S", "Trackbar Windows")
         ms = 121 #cv2.getTrackbarPos("min_S", "Trackbar Windows")
         Mv = 255 #cv2.getTrackbarPos("max_V", "Trackbar Windows")
         mv = 225  #cv2.getTrackbarPos("min_V", "Trackbar Windows")
            
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
         cv2.imshow('befo', Masked)
         cv2.imshow('mask', Mask)
         #cv2.drawContours(frame, line[1], -1, (255,255,255), 3)
         cv2.imshow('visual', frame)
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
        TX_data_py2(serial_port, 3) #Right turn 5
    elif int(x)<280 and c_x!=0 :
        TX_data_py2(serial_port, 1) #Left turn 5
        
def set_ball_center2(x):
    if int(x)>360:
        #set_serial()
        #serial_port.write(serial.to_bytes([9]))
        TX_data_py2(serial_port, 42) #Right turn 5
    elif int(x)<280 and c_x!=0 :
        TX_data_py2(serial_port, 41) #Left turn 5

def set_ball_hit(x):
    if int(x)>490:
        #set_serial()
        #serial_port.write(serial.to_bytes([9]))
        TX_data_py2(serial_port, 42) #Right sidestep 10
    elif int(x)<410 and c_x!=0 :
        TX_data_py2(serial_port, 41) #Left sidestep 10

def set_hole_hit(x):
    if float(x)>12: #실제 거리 기준으로는 17
        #set_serial()
        #serial_port.write(serial.to_bytes([9]))
        TX_data_py2(serial_port, 3) #Right turn 5
    elif float(x)<10 and c_x!=0 : #여기도 15
        TX_data_py2(serial_port, 1) #Left turn 5

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
doesnt_find=0
find_hole_cnt=0
set_cnt = 0
head_cnt = 60
rl_head_cnt = 0
if __name__ == "__main__":
    open_camera()   
    serial_port = set_serial()
    TX_data_py2(serial_port, 31)
    while True:
        print('set_cnt : ' + str(set_cnt))
        #print('head_cnt : ' + str(head_cnt))
        #print('set_cnt : ' + str(set_cnt)) 

        '''
        if rl_head_cnt == 0:
            c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball() #센터 맞추기
        elif rl_head_cnt == 90:
            c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole() #센터 맞추기
            #serial_port = set_serial()
        '''
        #print('cX : ' + str(c_x)+ ', '+'cY : '+ str(c_y)+', '+'disX : '+str(dist_x)+', '+'disY : '+str(dist_y)+', '+'distL : ' + str(dist_l))
        if set_num == 0: #Head up-down judge
            if rl_head_cnt == 0:
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball() #센터 맞추기
            elif rl_head_cnt == 90:
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole() #센터 맞추기

            if (head_cnt == 60 or head_cnt == 40):
                if (int(c_x) < 280 or int(c_x) > 360):
                    c_x, c_y, dist_x, dist_y, dist_l = get_point()
                    set_ball_center(c_x)
                    c_x, c_y, dist_x, dist_y, dist_l = get_point()
                elif int(c_y) < 400:
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                    TX_data_py2(serial_port, 11)
                    #cv2.waitKey(1)
                    TX_data_py2(serial_port,23)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
            elif head_cnt == 20:
                if set_cnt == 0:
                    set_ball_center2(c_x) #이거 set_ball_hit가 돌 상황에 이것도 돌게 됨.
                    c_x, c_y, dist_x, dist_y, dist_l = get_point()
                if head_cnt == 20 and int(c_y) < 10:
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                    TX_data_py2(serial_port, 10)
                    #cv2.waitKey(1)
                    TX_data_py2(serial_port,23)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()         
                elif head_cnt == 20 and int(c_y) >= 50:
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                    TX_data_py2(serial_port, 32)
                    #cv2.waitKey(1)
                    TX_data_py2(serial_port,23)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball() #이거 잘 작동하면 get_point함수로 교체
                if head_cnt == 20 and set_cnt > 0: #추가로 고치기
                    set_ball_hit(c_x)
                    c_x, c_y, dist_x, dist_y, dist_l = get_point()
            #if dist_l < 30: #거리 따라 다르게 걷기
            '''if (head_cnt == 60 or head_cnt == 40) and int(c_y) < 400:
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                TX_data_py2(serial_port, 11)
                #cv2.waitKey(1)
                TX_data_py2(serial_port,23)
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()'''

            '''if head_cnt == 20 and int(c_y) < 10:
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                TX_data_py2(serial_port, 10)
                #cv2.waitKey(1)
                TX_data_py2(serial_port,23)
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()         
            elif head_cnt == 20 and int(c_y) >= 50:
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
                TX_data_py2(serial_port, 32)
                #cv2.waitKey(1)
                TX_data_py2(serial_port,23)
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball() #이거 잘 작동하면 get_point함수로 교체'''
            

            if rl_head_cnt == 0 and head_cnt == 60 and int(c_y) >= 400 and set_cnt < 1:
                set_num = 1
            elif rl_head_cnt == 0 and head_cnt == 40 and int(c_y) >= 420 and set_cnt < 1:
                set_num = 2
            elif rl_head_cnt == 0 and head_cnt == 20 and int(c_x) > 280 and int(c_x) < 360 and set_cnt < 1:
                set_num = 3
                
            elif rl_head_cnt == 0 and head_cnt == 20 and int(c_x) > 410 and int(c_x) < 490 and set_cnt >= 1 and set_cnt < 3:#어차피 set_num = 3으로 가서 7이 돌기에 이 구문은 필요없고 여기서 처리하고 싶은 범위 설정을 277번 줄에서 해결할 것.
                set_num = 3
            elif rl_head_cnt == 0 and head_cnt == 20 and int(c_y) < 50 and  int(c_x) > 410 and int(c_x) < 490 and set_cnt > 2:
                set_num = 3

            

        elif set_num == 1:
            c_x, c_y, dist_x, dist_y, dist_l = None, None, None, None, None#Camera_distance_ball()
            rx_num = RX_data(serial_port)    
            TX_data_py2(serial_port, 37) #Head down 50
            c_x, c_y, dist_x, dist_y, dist_l = None, None, None, None, None#Camera_distance_ball()
            if int(rx_num) == 37:   
                set_num = 0
                #preset_num = 1
                head_cnt = 40
                V_angle = 40
            elif int(rx_num) != 37:
                print('rx_num is not 37') 

        elif set_num == 2:
            c_x, c_y, dist_x, dist_y, dist_l = None, None, None, None, None
            rx_num = RX_data(serial_port)    
            TX_data_py2(serial_port, 39) #Head down 50
            if int(rx_num) == 39:
                set_num = 0
                #preset_num = 2
                head_cnt = 20
                rl_head_cnt = 0
                V_angle = 20
            elif int(rx_num) != 39:
                print('rx_num is not 39')                        
        elif set_num == 3:
            
            c_x, c_y, dist_x, dist_y, dist_l = None, None, None, None, None
            rx_num = RX_data(serial_port)    
            TX_data_py2(serial_port, 31) 
            
            if int(rx_num) == 31:
                head_cnt = 60
                V_angle = 60
                set_num = 4 #0로 가면 볼 칠 수 있도록 세팅함. 
            elif int(rx_num) != 31: 
                print('rx_num is not 31')                        

        elif set_num == 4:
            c_x, c_y, dist_x, dist_y, dist_l = None, None, None, None, None
            rx_num = RX_data(serial_port)
            TX_data_py2(serial_port, 17) 
            if int(rx_num) == 17:
                rl_head_cnt == 90
                set_num = 5
            elif int(rx_num) != 17:
                print('rx_num is not 17')
                
        elif set_num == 5:
            if doesnt_find > 100:
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                print("find_hole_cnt : " + str(find_hole_cnt))
                print("dist_x : " + str(dist_x))
                if int(dist_x)!=0:
                    doesnt_find = 0
                    set_hole_hit(dist_x)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                    if float(dist_x) < 12.0 and float(dist_x) > 10.0 and set_cnt < 3:
                        set_num = 7
                    elif float(dist_x) < 12.0 and float(dist_x) > 10.0 and set_cnt > 2:
                        set_num = 8
                        
                elif int(dist_x) == 0 and find_hole_cnt < 2:
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                    if int(dist_x) == 0:
                        doesnt_find+=1
                        if doesnt_find > 50:
                            set_num=6
                            count_43=0
                            cant_receive=0
                            c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                    '''
                    if int(rx_num) == 43:
                        rx_num = RX_data(serial_port) 
                        find_hole_cnt=1
                    elif int(rx_num) != 43:
                        print('rx_num is not 43')
                    
                    find_hole(dist_x)
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                    find_hole_cnt+=1
                    '''
            else:
                doesnt_find+=1
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
        elif set_num == 6:
            c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()#None, None, None, None, None
            #print("coiunt_43 : " + str(count_43))
            rx_num = RX_data(serial_port)    
            if count_43 == 0:
                TX_data_py2(serial_port, 43)
                count_43+=1
                cant_receive=0
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
            if int(rx_num) == 43 or int(dist_x)!=0:
                set_num = 5
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                #preset_num = 2
                head_cnt = 60
                rl_head_cnt = 90
                V_angle = 60
            elif int(rx_num) != 43:
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                print("dist_x : " + str(dist_x))
                #print('rx_num is not 43') 
                cant_receive+=1
                if cant_receive > 100:
                    count_43=0
                    c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
            

        elif set_num == 7:
            c_x, c_y, dist_x, dist_y, dist_l = None, None, None, None, None #Camera_distance_ball()
            rx_num = RX_data(serial_port)    
            TX_data_py2(serial_port, 39)
            c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_ball()
            if int(rx_num) == 39:
                set_num = 0
                #preset_num = 2
                head_cnt = 20
                rl_head_cnt = 0
                V_angle = 20
                set_cnt = set_cnt + 1
            elif int(rx_num) != 39:
                print('rx_num is not 39')     
                    
        elif set_num == 8:
            c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
            print("find_hole_cnt : " + str(find_hole_cnt))
            print("dist_x : " + str(dist_x))
            if int(dist_x)!=0:
                set_hole_hit(dist_x)
                c_x, c_y, dist_x, dist_y, dist_l = Camera_distance_hole()
                if int(dist_x) < 12 and int(dist_x) > 10:
                    set_num = 9
        
        elif set_num == 9: #여기에 홀 align 맞추는 코드. set_num 4 에서 아마 쳐야할 듯.
            rx_num = RX_data(serial_port)
            TX_data_py2(serial_port, 45)
            if int(rx_num) == 45:
                break
            elif int(rx_num) != 45:
                print('rx_num is not 45')
                
            
            




        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
