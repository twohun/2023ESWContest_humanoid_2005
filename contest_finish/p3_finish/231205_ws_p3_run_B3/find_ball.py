from __init__ import *
import constant_value as const
from datetime import timedelta, datetime

class FIND_BALL():
    def __init__(self) -> None:
        pass

    def find_ball(self):
        iter = 54
        rotate_fun = 0
        set_num = 0
        pre_num = 0
        now = datetime.now()
        delay_time = 300000 #0.5s
  
        # 왼쪽 확인
        while True:
            CAMERA.show_image()
            c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_ball()
            # 고개 돌리면서 공확인
            if set_num == 0:
                # 왼쪽에서 공을 못찾으면 나오기
                if iter < 46:
                    break
                # 공찾으면 빠져 나오기
                if abs(c_x-320) < 200 and (c_y > 50):
                    TX_data_py2(SERIAL,23)
                    time.sleep(0.1)
                    TX_data_py2(SERIAL,55)
                    now = datetime.now()
                    delay_time = 1500000
                    while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                        CAMERA.show_image()
                    delay_time = 300000
                    rotate= 54 - iter  
                    set_num=2
                    pre_num = 1
                    now=datetime.now()
                # 공을 못찾으면 고개 돌리기
                else:
                    set_num = 2
                    pre_num = 0
                    TX_data_py2(SERIAL,iter)
                    iter=iter - 2
                    now=datetime.now()
            # 몸 돌리기
            elif set_num == 1:

                if const.FALLDOWN_FLAG == 1:
                    const.FALLDOWN_FLAG = 0
                    return False
                
                if rotate_fun <= rotate:
                    TX_data_py2(SERIAL,70)
                    set_num=2
                    pre_num=1
                    rotate_fun=rotate_fun + 2 
                    now=datetime.now()
                else:
                    return True
            # timer 기다리기
            elif set_num == 2:
                if(datetime.now()-now>timedelta(microseconds=delay_time)):
                    set_num=pre_num
        
        iter = 56
        set_num = 0
        rotate_fun=0
        TX_data_py2(SERIAL,55) # 고개 돌리기 초기 세팅 중앙으로
        now = datetime.now()
        delay_time = 1500000
        while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
            CAMERA.show_image()
        delay_time = 300000
        # 오른쪽 확인
        while True:
            CAMERA.show_image()
            c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_ball()
            # 고개 돌리면서 공확인
            if set_num == 0:
                # 왼쪽에서 공을 못찾으면 나오기
                if iter > 64:
                    break
                # 공찾으면 빠져 나오기 원래 150
                if abs(c_x-320) < 200 and (c_y > 50):
                    TX_data_py2(SERIAL,23)
                    time.sleep(0.1)
                    TX_data_py2(SERIAL,55)
                    rotate = iter - 56
                    set_num = 2
                    pre_num = 1
                    now=datetime.now()
                # 공을 못찾으면 고개 돌리기
                else:
                    set_num = 2
                    pre_num = 0
                    TX_data_py2(SERIAL,iter)
                    iter = iter + 2
                    now=datetime.now()
            # 몸 돌리기
            elif set_num == 1:
                if const.FALLDOWN_FLAG == 1:
                    const.FALLDOWN_FLAG = 0
                    return False
                
                if rotate_fun <= rotate:
                    TX_data_py2(SERIAL,72)
                    set_num=2
                    pre_num=1
                    rotate_fun=rotate_fun + 2
                    now=datetime.now()
                else:
                    return True
            # timer 기다리기
            elif set_num == 2:
                if(datetime.now()-now>timedelta(microseconds=delay_time)):
                    set_num=pre_num
        
    
    def main(self):

        delay = 1500000 #1.5s 고개는 돌리는데 오래걸려서

        const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
        for i in range(len(const.NECK_LIST)):
            self.print_neck_value()
            TX_data_py2(SERIAL, const.NECK_LIST[const.NECK_POINTER])
            now = datetime.now()
            while ((datetime.now()-now)<timedelta(microseconds=delay)):
                CAMERA.show_image()
                
            success = self.find_ball()
            if success:
                const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
                const.NECK_POINTER = 0
                return True
            try:
                const.NECK_POINTER = const.NECK_POINTER + 1
                const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
            except:
                
                delay = 2000000
                
                '''for i in range(3):
                    TX_data_py2(SERIAL,11)
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay)):
                        if const.FALLDOWN_FLAG == 1:
                            const.FALLDOWN_FLAG = 0
                            return False
                        CAMERA.show_image()

                TX_data_py2(SERIAL, 22)
                now = datetime.now()
                while ((datetime.now()-now)<timedelta(microseconds=delay)):
                    if const.FALLDOWN_FLAG == 1:
                        const.FALLDOWN_FLAG = 0
                        return False
                    CAMERA.show_image()'''
                

        return False
    
    def print_neck_value(self):

        print('robot angle : ', const.ROBOT_ANGLE)
        print('neck pointer : ', const.NECK_POINTER)
        print('neck value : ', const.NECK_VALUE)          
            
class FIND_BALL_REVISE():
    def __init__(self) -> None:
        pass

    def find_ball(self):
        for i in range(len(const.NECK_LIST)):
            c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_ball()
            
            # 목각도 갱신
            const.NECK_POINTER = i
            const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
            TX_data_py2(SERIAL, const.NECK_LIST[const.NECK_POINTER])
            # delay
            now = datetime.now()
            delay_time = 500000
            while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                CAMERA.show_image()
            
            # 공찾으면 빠져 나오기
            if (c_x != 0) and (c_y > 50):
                TX_data_py2(SERIAL,23)
                time.sleep(0.1)
                TX_data_py2(SERIAL,55)
                return True
        
        return False
    
    def rotate_robot(self, iter, mode):

        for i in range(iter):
            # 넘어졌나 확인
            if const.FALLDOWN_FLAG == 1:
                const.FALLDOWN_FLAG = 0
                return False
            
            # 돌기 왼쪽
            if mode == 0:
                TX_data_py2(SERIAL,70)
            # 돌기 오른쪽
            elif mode == 1:
                TX_data_py2(SERIAL,72)
            # delay
            delay = 1000000
            now = datetime.now()
            while ((datetime.now()-now)<timedelta(microseconds=delay)):
                CAMERA.show_image()

        return True
    
    def main(self):
        
        if const.HIT_NUM == 0:
            head_list = [39, 87, 86] # 중앙 오른쪽 왼쪽
        else: 
            head_list = [39, 86, 87] # 중앙 왼쪽 오른쪽

        TX_data_py2(SERIAL, 39)
        time.sleep(1)
        
        for iter_find in range(len(head_list)):

            TX_data_py2(SERIAL,23)
            time.sleep(0.1)
            # 고개 바꾸기
            TX_data_py2(SERIAL,head_list[iter_find])
            # delay
            delay = 2000000
            now = datetime.now()
            while ((datetime.now()-now)<timedelta(microseconds=delay)):
                CAMERA.show_image()
            # 공찾기
            sucess = self.find_ball()
            # 공을 찾았으면
            if sucess:
                # 고개 중앙으로
                TX_data_py2(SERIAL,23)
                time.sleep(0.1)
                TX_data_py2(SERIAL,55)
                # 딜레이
                delay = 1000000
                now = datetime.now()
                while ((datetime.now()-now)<timedelta(microseconds=delay)):
                    CAMERA.show_image()
                
                # 몸 돌기
                sucess2 = 0
                if iter_find == 0:
                    sucess2 = self.rotate_robot(0,0)
                elif iter_find == 1:
                    if const.HIT_NUM == 1:
                        sucess2 = self.rotate_robot(9,1)
                    else:
                        sucess2 = self.rotate_robot(9,0)
                elif iter_find == 2:
                    if const.HIT_NUM == 1: 
                        sucess2 = self.rotate_robot(9,0)
                    else:
                        sucess2 = self.rotate_robot(9,1)

                if sucess2:
                    return True
                else: 
                    return False
            # 공을 못찾았을때
            if sucess == False and iter_find == 2:
                TX_data_py2(SERIAL,39)
                time.sleep(0.5)
                TX_data_py2(SERIAL, 22)
                delay = 1500000     
                now = datetime.now()
                while ((datetime.now()-now)<timedelta(microseconds=delay)):
                    if const.FALLDOWN_FLAG == 1:
                        const.FALLDOWN_FLAG =0
                        return False
                    CAMERA.show_image()

        return False










                
     