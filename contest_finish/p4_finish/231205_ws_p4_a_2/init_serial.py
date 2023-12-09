# -*- coding: utf-8 -*-

import serial
import time
from threading import Thread
import constant_value as const

serial_use = 1

serial_port =  None
Read_RX =  0
receiving_exit = 1
threading_Time = 0.01

#-----------------------------------------------
def set_serial():
    BPS = 4800
    serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
    serial_port.flush()
    return serial_port
#----------------------------------------------- 
def TX_data_py2(ser, one_byte):  # one_byte= 0~255
    #ser.write(chr(int(one_byte)))          #python2.7
    ser.write(serial.to_bytes([one_byte]))  #python3
#-----------------------------------------------
def RX_data(ser):

    if ser.inWaiting() > 0:
        result = ser.read(1)
        RX = ord(result)
        return RX
    else:
        return 0
 
def Receiving(ser):
    global receiving_exit

    receiving_exit = 1

    while True:
        if receiving_exit == 0:
            break
        time.sleep(threading_Time)
        while ser.inWaiting() >  0:
            result = ser.read(1)
            RX = ord(result)
            print ("RX=" + str(RX))
            # -----  remocon 16 Code  Exit ------
            if RX == 16 or RX == 15: # 넘어졌을 때 RX로 바꿔야 됨
                const.RCV_RX = 16
                const.TASK_FLAG = 2
                const.FALLDOWN_FLAG = 1
                RX = 0
            if RX == 100:
                const.TASK_FLAG = 1
            
#-----------------------------------------------

if __name__ == '__main__':
    import platform
    import numpy as np
    import cv2
    import sys
    #-------------------------------------
    print ("-------------------------------------")
    print ("---- (2020-1-20)  MINIROBOT Corp. ---")
    print ("-------------------------------------")
   
    os_version = platform.platform()
    print (" ---> OS " + os_version)
    python_version = ".".join(map(str, sys.version_info[:3]))
    print (" ---> Python " + python_version)
    opencv_version = cv2.__version__
    print (" ---> OpenCV  " + opencv_version)
    print ("-------------------------------------")

    BPS =  4800  # 4800,9600,14400, 19200,28800, 57600, 115200

    #---------local Serial Port : ttyS0 --------
    #---------USB Serial Port : ttyAMA0 --------
    
       
    serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
    serial_port.flush() # serial cls
    print(serial_port)
    #---------------------------

    
    #serial_t = Thread(target=Receiving, args=(serial_port,))
    #serial_t.daemon = True
    #serial_t.start()
    #time.sleep(0.1) 
    #---------------------------
    
    # First -> Start Code Send 
    TX_data_py2(serial_port, 41)

    
    time.sleep(1)

    
    
    # -----  remocon 16 Code  Exit ------
    #while receiving_exit == 1:
    #    time.sleep(0.01)
    
    
    #---------------------------
    time.sleep(1)
    #print(serial_port.readline())
    print("Return DATA: " + str(RX_data(serial_port)))
    print ("-------------------------------------")    
   
    exit(1)
