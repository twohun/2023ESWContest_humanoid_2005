from __init__ import *
import constant_value as const
from datetime import timedelta, datetime
from find_ball import FIND_BALL_REVISE
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
    find_ball = FIND_BALL_REVISE()
    approch_ball = APPROCH_BALL()
    check_finish = CHECK_FINISH()
    rotate_robot =  ROTATE_ROBOT()
    array_shut = ARRAY_SHUT()
    hit_turn = HIT_TURN()

    serial_thread = Thread(target=Receiving, args=(SERIAL,))
    serial_thread.daemon = True
    serial_thread.start()
    TX_data_py2(SERIAL, 33)
    while True:
        CAMERA.show_image()
        print('tasks_count : ', tasks_count)
        print('task_flag : ', const.TASK_FLAG)
        print('delay_count : ', delay_count)
        

        if const.TASK_FLAG == 1 and const.RCV_RX != 16 :
            if tasks_count == 0:
                #print('처음 공치는거')
                TX_data_py2(SERIAL, 33)
                const.NECK_POINTER = 1
                time.sleep(1)
                const.ROBOT_ANGLE = 30
                tasks_count = 1
                for i in range(10):
                    TX_data_py2(SERIAL, 41) #왼쪽으로 10
                    delay_time = 1000000
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                        CAMERA.show_image()
            #공 찾기
            elif tasks_count == 1:
                const.NECK_POINTER = 0
                sucess_t1 = find_ball.main()
                if sucess_t1:
                    tasks_count = 2
            #공 접근
            elif tasks_count == 2: 
                sucess_t2 = approch_ball.main()
                if sucess_t2:
                    tasks_count = 3
            #공 들어갔나 확인
            elif tasks_count == 3:
                sucess_t3 = check_finish.main()
                if sucess_t3:
                    tasks_count = 99  #끝!
                    delay_time = 1500000
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                        CAMERA.show_image()
                    TX_data_py2(SERIAL, 76)
                else:
                    delay_time = 1500000
                    now = datetime.now()
                    while ((datetime.now()-now)<timedelta(microseconds=delay_time)):
                        CAMERA.show_image()
                    delay_time = 500000
                    TX_data_py2(SERIAL, 73)
                    const.TASK_FLAG = 0
                    tasks_count = 4        
            # 동심원 돌기
            elif tasks_count == 4:
                sucess_t4 = rotate_robot.main()
                if sucess_t4:
                    tasks_count = 5
            # 홀 어레이 맞추기
            elif tasks_count == 5:
                sucess_t5 = array_shut.main()
                if sucess_t5:
                    tasks_count = 6
            elif tasks_count == 6:
                sucess_t6 = hit_turn.main()
                if sucess_t6:
                    tasks_count = 2
                else:
                    tasks_count = 1
       
        elif const.TASK_FLAG == 0 and const.RCV_RX != 16:
            if delay_count == 0:
                if(datetime.now()-const.NOW>timedelta(microseconds=const.DELAY_TIME)): #DELAY_TIME defalut is 500000
                    delay_count=1
                    const.DELAY_TIME = 500000 # 다시 딜레이 시간을 0.5s로
            elif delay_count == 1:
                print('finish delay')
                const.TASK_FLAG = 1
                delay_count = 0
        
        elif const.TASK_FLAG == 2:
            const.RCV_RX = 0
            tasks_count = 1
            approch_ball.clear_value()
            array_shut.clear_value  ()


        
