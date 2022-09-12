#!/usr/bin/env python
# import required libs
import time
import RPi.GPIO as GPIO

class Stepper:
    def __init__(self,StepPinsArray):
        self.StepPins = StepPinsArray
        self.Seq = [[1,0,0,1],[1,0,0,0],[1,1,0,0],[0,1,0,0],
                    [0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1]]
        self.StepCount = len(self.Seq)
        self.StepDir = 1
        self.VerStepDir = 1
        self.WaitTime = 0.001
        self.StepCounter = 0
        GPIO.setmode(GPIO.BOARD)
        for pin in self.StepPins:
            print("Setup pins")
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)


    def start(self, centerdata, conflag, adjustbox,center):
        if conflag == 1:
            # auto
            self.AutoStepper(centerdata,center)
        elif conflag == 0:
            self.ManualStepper(adjustbox)
            
    def ManualStepper(self,Dir):
        if Dir < 0:
            self.StepDir = -1
        elif Dir > 0:
            self.StepDir = 1
        else:
            self.StepDir = 0

        for pin in range(0,4):
            xpin = self.StepPins[pin]
            if(self.Seq[self.StepCounter][pin] != 0):
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        self.StepCounter += self.StepDir

        if (self.StepCounter >= self.StepCount):
            self.StepCounter = 0
        if (self.StepCounter < 0):
            self.StepCounter = self.StepCount + self.StepDir
        time.sleep(self.WaitTime)
        
    def AutoStepper(self,Hordata,center):
        #left
        if Hordata - center < 0:
            self.StepDir = 1
        elif Hordata - center > 0:
            self.StepDir = -1
        elif Hordata - center == 0:
            self.StepDir = 0
        for pin in range(0,4):
            xpin = self.StepPins[pin]
            if(self.Seq[self.StepCounter][pin] != 0):
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        self.StepCounter += self.StepDir

        if (self.StepCounter >= self.StepCount):
            self.StepCounter = 0
        if (self.StepCounter < 0):
            self.StepCounter = self.StepCount + self.StepDir
        #time.sleep(self.WaitTime)
        if  abs(Hordata - center) < 20:
            time.sleep(0.05)
        else:
            time.sleep(0.01)
