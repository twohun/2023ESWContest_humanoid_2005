from __init__ import *
import constant_value as const
from datetime import timedelta, datetime
from find_ball import FIND_BALL
from approach_ball import APPROCH_BALL
from check_finish import CHECK_FINISH
from rotate_robot import ROTATE_ROBOT
from array_shut import ARRAY_SHUT
from hit_turn import HIT_TURN
"""
할일 넘어졌을때 변수 초기화 필요한 함수들이 있다. 
1. approach_ball

샷 코드 추가 및 다른 코드들 확인하기

"""
if __name__ == "__main__":
    import platform
    import sys
    #-------------------------------------
    print ("-------------------------------------")
    print ("(2023) intelligentHumanoid HYMECADDIE")
    print ("-------------------------------------")
    print ("")
    os_version = platform.platform()
    print (" ---> OS " + os_version)
    python_version = ".".join(map(str, sys.version_info[:3]))
    print (" ---> Python " + python_version)
    opencv_version = cv2.__version__
    print (" ---> OpenCV  " + opencv_version) 
    
    delay_count = 0
    tasks_count = 0
    find_ball = FIND_BALL()
    approch_ball = APPROCH_BALL()
    check_finish = CHECK_FINISH()
    rotate_robot =  ROTATE_ROBOT()
    array_shut = ARRAY_SHUT()
    hit_turn = HIT_TURN()

    serial_thread = Thread(target=Receiving, args=(SERIAL,))
    serial_thread.daemon = True
    serial_thread.start()
    
    while(True):
        pass
