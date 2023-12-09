from __init__ import *
import constant_value as const
from datetime import timedelta, datetime

class ARRAY_SHUT():
    def __init__(self) -> None:
        self.set_count = 0
        self.set_ball_mode = 0
        self.set_ball_count = 0
        self.short_flag = 0
    
    def clear_value(self):
        self.set_count = 0
        self.set_ball_mode = 0
        self.set_ball_count = 0
        self.short_flag = 0
        
    def set_hole(self):
        head_val = [40, 60, 80]
        head_list = [82, 80, 78]
        
        print('set_count : ', self.set_count)
        c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_hole()
        # 정렬 완료시
        if const.ROBOT_ANGLE == 40:
            if float(dist_x) <= 12.5 and float(dist_x) >= 11.5:
                if float(dist_y) <= 30: #세기 약하게 하려고
                    #TX_data_py2(SERIAL, 42)
                    self.short_flag = 1
                now = datetime.now()
                delay_time = 1500000
                while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                    CAMERA.show_image()
                delay_time = 500000
                TX_data_py2(SERIAL, 39) #머리 전방 20도 내리기
                const.NECK_POINTER = 0 # NECK_VALUE = [20, 30, 40, 50, 60, 70, 80]
                const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
                self.set_count = self.set_count + 1

                const.DELAY_TIME = 1500000
                
            #세팅 코드 추가해야함
            if dist_x > 12.5:
                TX_data_py2(SERIAL, 69) # 오른쪽턴 5
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
            elif dist_x < 11.5:
                TX_data_py2(SERIAL, 67) # 왼쪽 턴 5
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
        
        else:
            if float(dist_x) <= 15.5 and float(dist_x) >= 14.5:
                if float(dist_y) <= 30: #세기 약하게 하려고
                    self.short_flag = 1
                now = datetime.now()
                delay_time = 1500000
                while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                    CAMERA.show_image()
                delay_time = 500000
                TX_data_py2(SERIAL, 39) #머리 전방 20도 내리기
                const.NECK_POINTER = 0 # NECK_VALUE = [20, 30, 40, 50, 60, 70, 80]
                const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
                self.set_count = self.set_count + 1

                const.DELAY_TIME = 1500000
                
            #세팅 코드 추가해야함
            if dist_x > 15.5:
                TX_data_py2(SERIAL, 69) # 오른쪽턴 5
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
            elif dist_x < 14.5:
                TX_data_py2(SERIAL, 67) # 왼쪽 턴 5
                const.TASK_FLAG = 0
                const.NOW = datetime.now()

    def set_ball(self):
        head_val = [40, 60, 80]
        head_list = [82, 80, 78]
        
        c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_ball()
        # 공을 못찾으면 오른쪽으로
        if c_x == 0 and c_y == 0:
            TX_data_py2(SERIAL, 41) #오른쪽으로 10
            const.TASK_FLAG = 0
            const.NOW = datetime.now()
            return False
        #앞뒤 맞춤
        if self.set_ball_mode == 0:
            if c_y >= 150 and c_y <=170:
                self.set_ball_mode = 1
            elif c_y > 170:
                TX_data_py2(SERIAL, 12) #후진
                TX_data_py2(SERIAL,23)
                const.NOW = datetime.now()
                const.TASK_FLAG = 0
                const.DELAY_TIME = 1500000 # 2s
            elif c_y < 150:
                TX_data_py2(SERIAL, 11) #전진
                const.NOW = datetime.now()
                const.TASK_FLAG = 0
                const.DELAY_TIME = 1500000 # 2s
        #좌우 맞춤
        if self.set_ball_mode == 1:
            
            
            if c_x <= 390 and c_x >= 350:
                    self.set_ball_mode = 0
                    self.set_count += 1
                    now = datetime.now()
                    delay = 500000

                    const.NECK_POINTER = const.NECK_PREPOINTER
                    const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]

                    now = datetime.now()
                    delay = 1000000
                    while ((datetime.now()-now)<timedelta(microseconds=delay)):
                        CAMERA.show_image()

                    TX_data_py2(SERIAL, 73) #홀을 찾기 위해 고개 돌리기
                    
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay)):
                        CAMERA.show_image()
                    
                    now = datetime.now()
                    delay = 1000000
                    # 이 부분 고침 >> pre pointer << 이전에 홀찾을떄 각도 기억하고 있는 포인터 -두연
                    const.ROBOT_ANGLE = head_val[const.NECK_PREPOINTER]
                    TX_data_py2(SERIAL, head_list[const.NECK_PREPOINTER]) #홀을 찾기 위해 상하 고개 돌리기
                    
                    while ((datetime.now()-now)<timedelta(microseconds=delay)):
                        CAMERA.show_image()

                    self.set_ball_count = self.set_ball_count + 1

            elif c_x >= 390:
                TX_data_py2(SERIAL, 42) #오른쪽으로 10
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
            elif c_x <= 350:
                TX_data_py2(SERIAL, 41) #왼쪽으로 10
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
        return False
    def set_ball_lr(self):
        head_val = [40, 60, 80]
        head_list = [82, 80, 78]
        while True:
            c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_ball()
            if c_x <= 390 and c_x >= 350:
                if self.short_flag == 1:
                    TX_data_py2(SERIAL, 42)
                break

            elif c_x > 390:
                TX_data_py2(SERIAL, 42) #오른쪽으로 10
                now = datetime.now()
                delay = 500000
                while ((datetime.now()-now)<timedelta(microseconds=delay)):
                    CAMERA.show_image()
            elif c_x < 350:
                TX_data_py2(SERIAL, 41) #왼쪽으로 10
                now = datetime.now()
                delay = 500000
                while ((datetime.now()-now)<timedelta(microseconds=delay)):
                    CAMERA.show_image()
        
    def main(self):
        # 2번 진행하고 끝내기
        if self.set_count > 2:
            self.set_ball_mode = 0
            self.set_count = 0
            if const.HIT_NUM == 0:
                time.sleep(0.5)
                TX_data_py2(SERIAL, 72)
                time.sleep(0.5)
                TX_data_py2(SERIAL, 72)
                time.sleep(0.5)
            self.set_ball_lr()
            self.short_flag = 0
            return True

        if self.set_count % 2 == 0:
            self.set_hole()
        else:
            self.set_ball()    
        
        
        return False
