from __init__ import *
import constant_value as const
from datetime import timedelta, datetime

class APPROCH_BALL():
    def __init__(self) -> None:
        self.mode_count = 0

    def clear_value(self):
        self.mode_count = 0
        
    def set_ball_center(self,x):
        if int(x)>350:
            TX_data_py2(SERIAL, 69 + 3*int((const.NECK_POINTER/4))) #Right turn 5
        elif int(x)<290 and x!=0 :
            TX_data_py2(SERIAL, 67 + 3*int((const.NECK_POINTER/4))) #Left turn 5
    
    def print_info(self):
        if self.mode_count == 0:
            print('approch init')
        elif self.mode_count == 1:
            print('공가운데 정렬')
        elif self.mode_count == 2:
            print('걷기')
    
    def print_neck_value(self):

        print('robot angle : ', const.ROBOT_ANGLE)
        print('neck pointer : ', const.NECK_POINTER)
        print('neck value : ', const.NECK_VALUE)
            
    def main(self):

        
        self.print_info()
        self.print_neck_value()
        c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_ball()
        const.DELAY_TIME = 200000
        
        if self.mode_count == 0:
            const.NECK_POINTER = int((int(const.ROBOT_ANGLE)/10 - 2))
            self.mode_count = 1
        # 공 가운데 정렬
        elif self.mode_count == 1:
            if abs(c_x-320) > (30 + const.NECK_POINTER*10):
                self.set_ball_center(c_x)
                const.TASK_FLAG = 0
                const.NOW = datetime.now()
            else:
                self.mode_count = 2
        elif self.mode_count == 2:
            # 일정 범위 이상일때는 60도 이상
            if const.NECK_POINTER > 3:
                if int(c_y) < 380 and int(c_y) > 0:
                    TX_data_py2(SERIAL, 10) #걷기
                    #TX_data_py2(SERIAL,23) # 멈춤
                    # const.TASK_FLAG = 0
                    self.mode_count = 1 #다시 공 가운데 정렬
                    const.NOW = datetime.now()
                else:
                    TX_data_py2(SERIAL,23)
                    time.sleep(0.2)
                    print('목 내리기')
                    const.NECK_POINTER = const.NECK_POINTER -1
                    const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
                    TX_data_py2(SERIAL,const.NECK_LIST[const.NECK_POINTER])
                    const.TASK_FLAG = 0
                    const.DELAY_TIME = 1500000 #목내리는데 충분한 시간을 주기위해 딜레이 시간을 1s로
                    const.NOW = datetime.now()
                    
            else:
                if int(c_y) < 250 and int(c_y) > 0:
                    TX_data_py2(SERIAL, 10) #걷기
                    TX_data_py2(SERIAL,23) # 멈춤
                    # const.TASK_FLAG = 0
                    self.mode_count = 1 #다시 공 가운데 정렬
                    const.NOW = datetime.now()
                else:
                    # 공에 충분히 가까워 졌다면 30도 이하
                    TX_data_py2(SERIAL,23)
                    time.sleep(0.2)
                    if const.NECK_POINTER <2:
                        self.mode_count = 0
                        return True
                    print('목 내리기')
                    const.NECK_POINTER = const.NECK_POINTER -1
                    const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
                    TX_data_py2(SERIAL,const.NECK_LIST[const.NECK_POINTER])
                    const.TASK_FLAG = 0
                    const.DELAY_TIME = 1000000
                    const.NOW = datetime.now()
        
        return False
                    

            
             
