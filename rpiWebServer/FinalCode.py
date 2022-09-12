import sys,time,serial
import RPi.GPIO as GPIO

class helmet:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.Center = 0
        self.Left = 0
        self.Right = 0
        self.StepPins = [29,31,32,33]
        self.Seq = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
                    [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
        self.StepCount = len(self.Seq)
        self.StepDir = 1
        self.WaitTime = 0.001
        self.StepCounter = 0
        self.Steps = 1
        self.Port = "/dev/rfcomm0"
        self.SerialCon = serial.Serial(self.Port,9600)

    def InitCoordinate(self):
        try:
            print("Initialize Start")
            self.Center = self.InitTurnCenter()
            self.Left = self.InitTurnLeft()
            self.Right = self.InitTurnRight()
            print("Center:",self.Center," Left:",self.Left," Right:",self.Right)
            self.CalculateRange()
        except Exception as e:
            print(str(e))
        finally:
            self.SerialCon.write(bytes("OK".encode()))

    # To initialize
    def InitTurnCenter(self):
        self.SerialCon.flushInput()
        self.SerialCon.flushOutput()
        print("Now init!")
        CenterValue = []
        Times = 0
        Can_Go = 0
        # Talk to arduino want to initialize
        self.SerialCon.write(bytes("Initialize".encode()))
        while True:
            time.sleep(1)
            Line = self.SerialCon.inWaiting()
            if(Line):
                Check = self.SerialCon.readline(Line).decode("unicode_escape")
                if(Check == "Initialize"):
                    Can_Go = 1
                    self.SerialCon.write(bytes("GetData".encode()))
                elif(Can_Go == 1):
                    Check = float(Check)
                    if( Times >= 5 ):
                        CenterValue.append( Check )
                    Times += 1
                    if(Times == 15):
                        self.SerialCon.write(bytes("Clear".encode()))
                        CenterValue = self.CalculateMaxMin(CenterValue)
                        break
        print("init end!")
        return float(CenterValue)

    # To left
    def InitTurnLeft(self):
        self.SerialCon.flushInput()
        self.SerialCon.flushOutput()
        print("Now left!")    
        LeftValue = []
        Times = 0
        time.sleep(3)
        self.SerialCon.write(bytes("GetData".encode()))
        while True:
            time.sleep(1)
            Line = self.SerialCon.inWaiting()
            if(Line):
                Check = self.SerialCon.readline(Line).decode("unicode_escape")
                Check = float(Check)
                LeftValue.append(Check)
                Times += 1
                if(Times == 10):
                    self.SerialCon.write(bytes("Clear".encode()))
                    LeftValue = self.CalculateMaxMin(LeftValue)
                    break
        return float(LeftValue)

    def InitSensor(self):
        self.SerialCon.flushInput()
        self.SerialCon.flushOutput()
        print("Start Init Sensor!")
        self.SerialCon.write(bytes("InitSensor".encode()))
        time.sleep(3)
        while True:
            time.sleep(1)
            Line = self.SerialCon.inWaiting()
            if(Line):
                Check = self.SerialCon.readline(Line).decode("unicode_escape")
                print(Check)
                print(Check == "Initialize Sensor finish")
                if(Check == "Initialize Sensor finish"):
                    break
        #return True

    # To right
    def InitTurnRight(self):
        self.SerialCon.flushInput()
        self.SerialCon.flushOutput()
        print("Now right!")
        right_value = []
        Times = 0
        time.sleep(3)
        self.SerialCon.write(bytes("GetData".encode()))
        while True:
            time.sleep(1)
            Line = self.SerialCon.inWaiting()
            if(Line):
                Check = self.SerialCon.readline(Line).decode("unicode_escape")
                Check = float(Check)
                right_value.append(Check)
                Times += 1
                if(Times == 13):
                    self.SerialCon.write(bytes("Clear".encode()))
                    right_value = self.CalculateMaxMin(right_value)
                    break
        return float(right_value)

    def CalculateMaxMin(self,value):
        Total = 0
        print(value)
        for i in range(0,10,1):
            if( not (value[i] == max(value) or value[i] == min(value)) ):
                Total += value[i]
        return Total/8

    def CalculateRange(self):
        if(self.Center > 0):
            self.RangeRight = (self.Center + self.Right)
            self.RangeLeft = (self.Left - self.Center)
        else:
            self.RangeRight = (self.Center + self.Right)
            self.RangeLeft = (self.Center + self.Left)
        return True

    def Move(self):
        #time.sleep(2)
        status = False
        self.SerialCon.flushInput()
        self.SerialCon.flushOutput()
        #50度 640 => 1:12.8
        self.SerialCon.write(bytes("GetData".encode()))
        try:
            while True:
                Line = self.SerialCon.inWaiting()
                if(Line):
                    turn = self.SerialCon.readline(Line).decode("unicode_escape")
                    print("turn",turn)
                    turn = float(turn)
                    if(self.Center <= turn ):
                        #*(-180-turn)/(5.625/64)
                        #print(int(self.RangeRight))
                        status = self.StepperRun(1)
                    elif ( turn < self.Center ):
                        #*(180-turn)/(5.625/64)
                        #print(int(self.RangeLeft))
                        status = self.StepperRun(-1)
                print("Back")
                #time.sleep(0.5)
        except Exception as e:
            self.SerialCon.write(bytes("Clear".encode()))
            print(e)
            #self.Move()

    def SetupStepper(self):
        for pin in self.StepPins:
            print("Setup pins")
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
    
    def StepperRun(self,angles):
        if(angles < 0):
            self.StepDir = -1
        else:
            self.StepDir = 1
        try:
            print("Angles",angles)
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
            return True
        except Exception as e:
            print(e)
            self.SerialCon.write(bytes("Clear".encode()))
        '''
        finally: #cleaning up and setting pins to low again (motors can get hot if you wont) 
            print("Error Run")
            self.SerialCon.write(bytes("Clear".encode()))
            GPIO.setmode(GPIO.BOARD)
            for pin in self.StepPins:
                GPIO.setup(pin,GPIO.OUT)
                GPIO.output(pin, False)'''

GPIO.setwarnings(False)
GPIO.cleanup()
Helmet = helmet()
while True:
    print("Choose your action")
    print("1:Initialize Sensor")
    print("2:Initialize Coordinate")
    print("3:Setup Stepper")
    print("4:Start to Move")
    choose = int(input("Your action is: "))
    if choose == 1:
        Helmet.InitSensor()
    elif choose == 2:
        Helmet.InitCoordinate()
    elif choose == 3:
        Helmet.SetupStepper()
    elif choose == 4:
        Helmet.Move()
    else:
        print("Error")
        print("")
