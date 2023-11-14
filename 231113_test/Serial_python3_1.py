# -*- coding: utf-8 -*-

import platform
import numpy as np
import argparse
import cv2
import serial
import time
import sys
from threading import Thread


serial_use = 1

serial_port =  None
Read_RX =  0
receiving_exit = 1
threading_Time = 0.01

#-----------------------------------------------

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
 
#-----------------------------------------------

# *************************
def Receiving(ser):
    global receiving_exit

    global X_255_point
    global Y_255_point
    global X_Size
    global Y_Size
    global Area, Angle


    receiving_exit = 1
    while True:
        if receiving_exit == 0:
            break
        time.sleep(threading_Time)
        while ser.inWaiting() > 0:
            result = ser.read(1)
            RX = ord(result)
            print ("RX=" + str(RX))
            
            # -----  remocon 16 Code  Exit ------
            if RX == 16:
                receiving_exit = 0
                break
            


# **************************************************
# **************************************************
# **************************************************
if __name__ == '__main__':

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








