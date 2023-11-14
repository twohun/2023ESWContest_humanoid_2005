import time
import numpy as np
import cv2 
from math import *
#from Hypepara import *
import platform
import argparse
import serial
import time
import sys
from threading import Thread

state_comm = 2  #//0 com1 //1: com7 //2~: false comm
#action = 'marathon'
#action = 'curling'
#action = 'debug'
action = 'callib_cam'

#action_opt = 'cam_on'
action_opt = 'cam_off'

X = 640
Y = 480

W_angle = 24.273#29.5
H_angle = 19.013#22.6

V_angle = 60 #기본자세 머리 각도. 231012 기준

Robot_height = 32.5
