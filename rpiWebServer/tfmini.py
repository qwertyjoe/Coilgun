import serial
import time

class tfmini:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
        #ser.write(0x42)
        self.ser.write(bytes(b'B'))
        #ser.write(0x57)
        self.ser.write(bytes(b'W'))
        #ser.write(0x02)
        self.ser.write(bytes(2))
        #ser.write(0x00)
        self.ser.write(bytes(0))
        #ser.write(0x00)
        self.ser.write(bytes(0))
        #ser.write(0x00)
        self.ser.write(bytes(0))
        #ser.write(0x01)
        self.ser.write(bytes(1))
        #ser.write(0x06)
        self.ser.write(bytes(6))
    def getdistance(self):
        self.ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
        self.ser.write(bytes(b'B'))
        self.ser.write(bytes(b'W'))
        self.ser.write(bytes(2))
        self.ser.write(bytes(0))
        self.ser.write(bytes(0))
        self.ser.write(bytes(0))
        self.ser.write(bytes(1))
        self.ser.write(bytes(6))
        while(True):
            while(self.ser.in_waiting >= 9):
                if( (b'Y' == self.ser.read()) and (b'Y' == self.ser.read()) ):
                    Dist_L = self.ser.read()
                    print("Dist_L",Dist_L)
                    Dist_H = self.ser.read()
                    print("Dist_H",Dist_H)
                    Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                    for i in range (0,5):
                        self.ser.read()
                    self.ser.close()
                    return Dist_Total

