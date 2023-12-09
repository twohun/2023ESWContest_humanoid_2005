from __init__ import *
import constant_value as const
from datetime import timedelta, datetime

class CHECK_FINISH():
    def __init__(self) -> None:
        pass
    
    def check_ball(self):
        ball_x, ball_y, ball_dist_x, ball_dist_y, ball_dist_l = CAMERA.get_info_ball()
        hole_x, hole_y, hole_dist_x, hole_dist_y, hole_dist_l = CAMERA.get_info_hole()

        if abs(ball_x-hole_x) < 80 and abs(ball_y-hole_y) < 80:
            print('done')
            return True
        else:
            return False
        
    def main(self):
        suscess = self.check_ball()
        if suscess:
            return True
        else:
            return False        
    