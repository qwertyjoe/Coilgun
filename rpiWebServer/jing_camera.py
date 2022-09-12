import cv2
import argparse
import glob
import numpy as np
import os
import time
import sys
import threading
basedir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basedir, os.path.pardir)))
from tracker import re3_tracker
from re3_utils.util import drawing
from re3_utils.util import bb_util
from re3_utils.util import im_util
import DottedFrame
from constants import OUTPUT_WIDTH
from constants import OUTPUT_HEIGHT
from constants import PADDING
# import test_stepper
import CAMstepper
import ServoGpio
import driver_camera_lib


class VideoCamera(object):
    def __init__(self, flip = False):
        self.CamNum = 0
        self.cam = cv2.VideoCapture(self.CamNum)
        self.cam.set(cv2.CAP_PROP_FPS, 30)
        self.outputBoxToDraw = None
        self.boxToDraw = np.zeros(4)
        self.x = 320
        self.y = 240
        self.time_count = 0
        self.track_sign = 0
        self.tracker = re3_tracker.Re3Tracker()
        self.StartFrameTime = 0
        self.PrevFrameTime = 0
        self.size = 50
        self.StartCoordinate = (self.x-self.size,self.y-self.size)
        self.EndCoordinate = (self.x+self.size,self.y+self.size)
        self.ChangeStatus = -1 
        self.defaultboxcenter = (320,240)
        #Control Camera Angle Position
        self.Vertical = 0
        self.fps=30
        self.AdjustFlag = 0
        self.CurHorAngle = 0
        self.ManualShotFlag = 0
        #self.hstepper = CAMstepper.Stepper([29,31,32,33])
        try:
            self.ServoStepper = ServoGpio.PCA9685()
            self.StartAngle = 80
        except:
            print("\x1b[31m",'Warning: PCA9685 Fail!',"\x1b[39m")
    def camera_reset(self,num):
        self.cam = None
        self.CamNum = num
        time.sleep(0.1)
        self.cam = cv2.VideoCapture(self.CamNum)
        self.cam.set(cv2.CAP_PROP_FPS, 30)
    def parabola(self,stepps):
        self.ServoStepper.VStartAngle = steppsW

    ''' 
    def parabola(self,stepps):
        temp_wait = self.vstepper.WaitTime
        self.vstepper.WaitTime=0.001
        dir = 1
        if stepps<0:
            dir = -1
            stepps*= -1
        for i in range(stepps):
            # print(i)
            self.vstepper.ManualStepper(dir)
            self.vstepper.ManualStepper(dir)
        self.vstepper.WaitTime=temp_wait
    '''

    def startthread(self):
        hsend = threading.Thread(target=self.sendhorcoordinate)
        hsend.start()
        vsend = threading.Thread(target=self.sendvercoordinate)
        vsend.start()

    def sendhorcoordinate(self):
        # hstepper = CAMstepper.Stepper([29,31,32,33])
        while True:
            boxcenter = self.defaultboxcenter[0]
            if self.track_sign == 1:
                self.ServoStepper.StartHorzion(boxcenter)
            time.sleep(0.1)
    def sendvercoordinate(self):
        while True:
            boxcenter = self.defaultboxcenter[1]
            adjustbox = self.Vertical
            conflag = self.track_sign
            if conflag == 1:
                self.ServoStepper.StartVertical(boxcenter,conflag)
                time.sleep(0.05)
            if conflag == 0:
                self.ServoStepper.StartVertical(adjustbox,conflag)
                time.sleep(0.0075)
            if self.ManualShotFlag == 1:
                time.sleep(1.5)
                self.ManualShotFlag = 0

            

    def show_webcam(self):
        while True:
            self.StartFrameTime = time.time()
            ret_val, img = self.cam.read()
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            if not self.ChangeStatus == -1:
                self.BoxAdjust()
            if self.track_sign==1:
                if self.time_count=="1":
                    self.boxToDraw = (self.x-self.size,self.y-self.size,self.x+self.size,self.y+self.size)
                    self.outputBoxToDraw = self.tracker.track('webcam', img[:,:,::-1], self.boxToDraw)
                    self.time_count = "0"
                else:
                    self.outputBoxToDraw = self.tracker.track('webcam', img[:,:,::-1])
                cv2.rectangle(img,
                        (int(self.outputBoxToDraw[0]), int(self.outputBoxToDraw[1])),
                        (int(self.outputBoxToDraw[2]), int(self.outputBoxToDraw[3])),
                        [0,0,255], PADDING)
                self.defaultboxcenter = (
                        (int(self.outputBoxToDraw[0])+int(self.outputBoxToDraw[2]))/2 , 
                        (int(self.outputBoxToDraw[1])+int(self.outputBoxToDraw[3]))/2
                    )
            else:
                self.defaultboxcenter = (320,240)
                DottedFrame.drawrect(img,self.StartCoordinate,self.EndCoordinate,(0,0,255),1,'dotted')
            self.fps = 1/(self.StartFrameTime - self.PrevFrameTime)
            self.PrevFrameTime = self.StartFrameTime
            fps = str(int(self.fps))
            cv2.putText(img, fps, (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
            rect,jpeg = cv2.imencode('.jpg',img)
            return jpeg.tobytes()
    def BoxAdjust(self):
        if self.ChangeStatus == 1:
            self.size -= 2
            self.StartCoordinate = (self.x-self.size,self.y-self.size)
            self.EndCoordinate = (self.x+self.size,self.y+self.size)
        elif self.ChangeStatus == 0:
            self.size += 2
            self.StartCoordinate = (self.x-self.size,self.y-self.size)
            self.EndCoordinate = (self.x+self.size,self.y+self.size)

