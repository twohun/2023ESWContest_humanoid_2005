from __init__ import *
import constant_value as const
from datetime import timedelta, datetime
     
            
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

        if const.HIT_NUM == 1:
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










                
     