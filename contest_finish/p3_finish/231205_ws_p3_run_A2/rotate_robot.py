from __init__ import *
import constant_value as const
from datetime import timedelta, datetime

class ROTATE_ROBOT:
    
    def __init__(self) -> None:
        pass

    def check_hole(self):
       

        #head_val = [80, 60, 40]
        #head_list = [78, 80, 82]
        head_val = [40, 60]
        head_list = [82, 80]
        delay_time = 500000 #0.5s

        for i in range(2):
            TX_data_py2(SERIAL, head_list[i])
            
            # 고개 돌리고 잠깐 기다림
            now = datetime.now()
            delay_time = 500000
            while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                CAMERA.show_image()
            
            # 고개 확인
            c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_hole()

            if (c_x != 0 or (c_y != 0 and c_y > 50)): # 인식하면
                const.ROBOT_ANGLE = head_val[i]
                # 여기 고침 i >> 0 to 2 - 두연
                const.NECK_POINTER = i #  [40, 60, 80]
                const.NECK_PREPOINTER = const.NECK_POINTER
                
                return True

        return False 



    def rotate_around_ball(self):
        delay_time = 3000000 #3s
        TX_data_py2(SERIAL, 43)
        now = datetime.now()
        while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                CAMERA.show_image()

    
    def main(self):
        while True:
            # 넘어짐 판단
            if const.FALLDOWN_FLAG == 1:
                const.FALLDOWN_FLAG = 0
                break
            
            CAMERA.show_image()
            
            sucess = self.check_hole()
            
            if sucess:
                return True
            else:
                self.rotate_around_ball()
