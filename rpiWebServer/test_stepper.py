#!/usr/bin/env python
# import required libs
import time
import RPi.GPIO as GPIO

def AutoStepper(StepDir,status):
  GPIO.cleanup() #cleaning up in case GPIOS have been preactivated

  # Use BCM GPIO references
  # instead of physical pin numbers
  GPIO.setmode(GPIO.BOARD)

  # be sure you are setting pins accordingly
  # GPIO10,GPIO9,GPIO11,GPI25
  StepPins = [29,31,32,33]
  #StepPins = [11,12,13,15] 
  # Set all pins as output
  for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

   #wapinit some time to start
  #time.sleep(0.5)
     # Define some settings
  StepCounter = 0
  WaitTime = 0.0015

  # Define advanced sequence
  # as shown in manufacturers datasheet
  StepCount2 = 8
  Seq2 = list(range(0,8))
  Seq2[0] = [1,0,0,0]
  Seq2[1] = [1,1,0,0]
  Seq2[2] = [0,1,0,0]
  Seq2[3] = [0,1,1,0]
  Seq2[4] = [0,0,1,0]
  Seq2[5] = [0,0,1,1]
  Seq2[6] = [0,0,0,1]
  Seq2[7] = [1,0,0,1]

  # set
  Seq = Seq2
  StepCount = StepCount2
  i=0
  # Start main loop
  try:
    while status:
      for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          #print(" Step %i Enable %i" %(StepCounter,xpin))
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)
      StepCounter += StepDir
      #time.sleep(1)
      #ttt += 1
      i+=1
      if i==60:
        StepDir = DirectionChange(i)
        i=0
      #if(ttt == 512):
      #   break
    # If we reach the end of the sequence
    # start again
      if (StepCounter == StepCount):
        StepCounter = 0
      if (StepCounter < 0):
        StepCounter = StepCount + StepDir
      if StepDir == 0 :
        status = False
      else :
        status = True
    # Wait before moving on
      time.sleep(WaitTime)
    #  time.sleep(1)
  except:
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    for pin in StepPins:
        GPIO.setup(pin,GPIO.OUT) #print(" Step %i Enable %i" %(StepCounter,xpin))
        GPIO.output(pin, False)
  finally: #cleaning up and setting pins to low again (motors can get hot if you wont) 
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    for pin in StepPins:
      GPIO.setup(pin,GPIO.OUT)
      GPIO.output(pin, False)
def init():
  GPIO.cleanup() #cleaning up in case GPIOS have been preactivated
  # Use BCM GPIO references
  # instead of physical pin numbers
  GPIO.setmode(GPIO.BOARD)

  # be sure you are setting pins accordingly
  # GPIO10,GPIO9,GPIO11,GPI25
  StepPins = [29,31,32,33]
  #StepPins = [11,12,13,15] 
  # Set all pins as output
  for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

   #wait some time to start
  # time.sleep(0.5)
     # Define some settings
  StepCounter = 0
  WaitTime = 0.0015
  # Define advanced sequence
  # as shown in manufacturers datasheet
  StepCount2 = 8
  Seq2 = list(range(0,8))
  Seq2[0] = [1,0,0,0]
  Seq2[1] = [1,1,0,0]
  Seq2[2] = [0,1,0,0]
  Seq2[3] = [0,1,1,0]
  Seq2[4] = [0,0,1,0]
  Seq2[5] = [0,0,1,1]
  Seq2[6] = [0,0,0,1]
  Seq2[7] = [1,0,0,1]
  # set
  Seq = Seq2
  StepCount = StepCount2
  i=0

def ManualStepper(adjustbox):
  Horziontal = adjustbox[0]
  Vertical = adjustbox[1]
  # Start main loop
  try:
    if Horziontal == 1:
      StepDir = 1
      while i<=40:
        for pin in range(0, 4):
          xpin = StepPins[pin]
          if Seq[StepCounter][pin]!=0:
            #print(" Step %i Enable %i" %(StepCounter,xpin))
            GPIO.output(xpin, True)
          else:
            GPIO.output(xpin, False)
        StepCounter += StepDir
      # If we reach the end of the sequence
      # start again
        if (StepCounter == StepCount):
          StepCounter = 0
        if (StepCounter < 0):
          StepCounter = StepCount + StepDir
      # Wait before moving on
        time.sleep(WaitTime)
        i+=1
    elif Horziontal == -1:
      StepDir = -1
      while i<=40:
        for pin in range(0, 4):
          xpin = StepPins[pin]
          if Seq[StepCounter][pin]!=0:
            #print(" Step %i Enable %i" %(StepCounter,xpin))
            GPIO.output(xpin, True)
          else:
            GPIO.output(xpin, False)
        StepCounter += StepDir
      # If we reach the end of the sequence
      # start again
        if (StepCounter == StepCount):
          StepCounter = 0
        if (StepCounter < 0):
          StepCounter = StepCount + StepDir
    # Wait before moving on
        time.sleep(WaitTime)
        i+=1
    #  time.sleep(1)
  except:
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    for pin in StepPins:
        GPIO.setup(pin,GPIO.OUT) #print(" Step %i Enable %i" %(StepCounter,xpin))
        GPIO.output(pin, False)
  finally: #cleaning up and setting pins to low again (motors can get hot if you wont) 
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    for pin in StepPins:
      GPIO.setup(pin,GPIO.OUT)
      GPIO.output(pin, False)
def getcoordinate(centerdata,conflag,adjustbox):
    print('hello')
    LoadingFlag = False
    status = False
    Xcenter = centerdata[0]
    Ycenter = centerdata[1]
    MoveStatus = 0
    if conflag == 1:
      status = True
      if LoadingFlag == False:
        LoadingFlag = True
        if 320 - Xcenter < 0 and 320 - Xcenter < -10 :
          #turn right
          StepDir = -1
          if MoveStatus != StepDir :
            AutoStepper(StepDir,status)
            MoveStatus = DirectionChange(StepDir)
        elif 320 - Xcenter > 0 and 320 -Xcenter > 10:
          #turn left
          StepDir = 1
          if MoveStatus != StepDir :
            AutoStepper(StepDir,status)
            MoveStatus = DirectionChange(StepDir)
      else :
        if 320 - Xcenter < 0 and 320 - Xcenter < -10 :
          StepDir = -1
          if MoveStatus != StepDir :
            MoveStatus = DirectionChange(StepDir)
        elif 320 - Xcenter > 0 and 320 - Xcenter > 10 :
          StepDir = 1
          if MoveStatus != StepDir :
            MoveStatus = DirectionChange(StepDir)
    elif conflag == 0:
      if LoadingFlag == True:
        init()
        status = False
        StepDir = 0
        AutoStepper(StepDir,status)
        MoveStatus = DirectionChange(StepDir)
        LoadingFlag = False
      elif LoadingFlag == False:
        ManualStepper(adjustbox)
def DirectionChange(ChangeSign) :
    if ChangeSign != 80:
      StepDir = ChangeSign
      return StepDir
    else :
      return StepDir