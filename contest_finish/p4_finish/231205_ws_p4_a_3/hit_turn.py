from __init__ import *
import constant_value as const
from datetime import timedelta, datetime

class HIT_TURN():
    def __init__(self) -> None:
        pass
    
    def hit_ball(self):# 앞 뒤 딜레이 1초
        delay = 1000000
        now = datetime.now()
        while ((datetime.now()-now)<timedelta(microseconds=delay)):
            CAMERA.show_image()
        if const.HIT_NUM == 0 or const.HIT_NUM == 1:
            TX_data_py2(SERIAL, 45)
            const.HIT_NUM = const.HIT_NUM + 1
        elif const.HIT_NUM > 1:
            TX_data_py2(SERIAL, 45)
            const.HIT_NUM = const.HIT_NUM + 1
        
        delay = 8000000
        now = datetime.now()
        while ((datetime.now()-now)<timedelta(microseconds=delay)):
            CAMERA.show_image()

    def run_away(self, delay_time):
        delay = delay_time
        now = datetime.now()
        TX_data_py2(SERIAL, 10)
        while ((datetime.now()-now)<timedelta(microseconds=delay)):
            if const.FALLDOWN_FLAG == 1:
                const.FALLDOWN_FLAG =0
                return False
            CAMERA.show_image()
            c_x, c_y, dist_x, dist_y, dist_l = CAMERA.get_info_ball()
            if abs(c_x-320) < 200 and c_y > 100:
                return True
        TX_data_py2(SERIAL, 23)
        time.sleep(0.1) 
        return False




    def turn_left(self):
        delay = 2000000
        now = datetime.now()
        while ((datetime.now()-now)<timedelta(microseconds=delay)):
            CAMERA.show_image()

        TX_data_py2(SERIAL, 22)
        delay = 1500000     
        now = datetime.now()
        while ((datetime.now()-now)<timedelta(microseconds=delay)):
            if const.FALLDOWN_FLAG == 1:
                const.FALLDOWN_FLAG =0
                return False
            CAMERA.show_image()

        TX_data_py2(SERIAL, 22)
        delay = 1500000        
        now = datetime.now()
        while ((datetime.now()-now)<timedelta(microseconds=delay)):
            if const.FALLDOWN_FLAG == 1:
                const.FALLDOWN_FLAG =0
                return False
            CAMERA.show_image()
            
        if const.HIT_NUM == 1:
            TX_data_py2(SERIAL, 22)
            delay = 1500000        
            now = datetime.now()
            while ((datetime.now()-now)<timedelta(microseconds=delay)):
                if const.FALLDOWN_FLAG == 1:
                    const.FALLDOWN_FLAG =0
                    return False
                CAMERA.show_image()

    def main(self):
        self.hit_ball()
        self.turn_left()
        TX_data_py2(SERIAL, 31)
        const.NECK_POINTER = 4
        const.ROBOT_ANGLE = const.NECK_VALUE[const.NECK_POINTER]
        time.sleep(1)
        success = None
        if const.HIT_NUM == 1:
            success = self.run_away(7000000)
        elif const.HIT_NUM == 2:
            success = self.run_away(5000000)
        if success:
            return True
        return False
