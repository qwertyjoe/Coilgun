#!/usr/bin/env python

import RPi.GPIO as GPIO
import smbus
import time
from sys import argv

class PCA9685:
    '''
    help_msg = 
    PCA9685 [option]
    option:
        up
        down
        reset
        info
        chon [channel]
        choff [channel]
        allch  [ value:0~4095 ]
        allchd [duty cycle]
        ch   [channel] [value:0~4095]
        chd  [channel] [duty cycle:0.0~100.0]
        rchd  [channel] [relative duty cycle:0.0~100.0]
    command :
    T:(us) --> delay time
    D(ch):(duty cycle: 0.0 ~ 100.0) --> set ch as duty cycle
    C(ch):(count : 0 ~ 4095) --> set ch as count
    ex: 
        'T:100 C1:1024 C15:2035 C13:999 C07:777 D09:55.5'
    '''


    ######################
    # REG POSITION 
    ######################


    __MODE1              = 0x00
    __MODE2              = 0x01
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALL_LED_ON_L       = 0xFA
    __ALL_LED_ON_H       = 0xFB
    __ALL_LED_OFF_L      = 0xFC
    __ALL_LED_OFF_H      = 0xFD


    ######################
    # MODE1 FUNCTION Bits
    ######################


    __RESTART            = 0x80
    __SLEEP              = 0x10
    __AI                 = 0x20
    __ALLCALL            = 0x01
    __INVRT              = 0x10
    __OUTDRV             = 0x04


    def __init__(self):
        self.Horzionch = 3
        self.Verticalch = 1
        self.addr = 0x40
        self.bus = smbus.SMBus(1)  # 1 : /dev/i2c-1
        self.setFreq(50)
        self.setAutoIncrement(1)
        self.HStartAngle = 85
        self.VStartAngle = 80
        self.StepDir = 0

    def getRegChOffH(self,channel):
        return self.bus.read_byte_data(self.addr, 4 * channel + self.__LED0_OFF_H)

    def setRegChOffL(self,channel,val):
        self.bus.write_byte_data(self.addr, channel * 4 + self.__LED0_OFF_L , val )

    def setRegChOffH(self,channel,val):
        self.bus.write_byte_data(self.addr, channel * 4 + self.__LED0_OFF_H  , val )

    def getRegMODE1(self):
        return self.bus.read_byte_data(self.addr, self.__MODE1)
    

    def setRegMODE1(self,val):
        self.bus.write_byte_data(self.addr, self.__MODE1, val)

    def setRegPrescale(self, _prescale):
        return self.bus.write_byte_data(self.addr, self.__PRESCALE, _prescale )

    def setAutoIncrement(self, val):
        if(val == 1):
            self.setRegMODE1(self.getRegMODE1() | self.__AI)
        elif(val == 0):
            self.setRegMODE1(self.getRegMODE1() &~ (self.__AI))

    def sleep(self):
        self.setRegMODE1( self.getRegMODE1() | self.__SLEEP) 
    
    def wakeup(self):
        self.setRegMODE1( self.getRegMODE1() &~ self.__SLEEP )

    def setValChOff(self, chan, off):

        if((off & 0xf000) > 0):
            print("error : too large value of off")
            return 

        _off_l =     off & 0x00ff
        _off_h = ( ( off & 0xff00 ) >> 8 ) | ( self.getRegChOffH(chan) & 0x10)

        self.setRegChOffL(chan , _off_l)
        self.setRegChOffH(chan , _off_h)

    def setFreq(self, freq):
        prescale_val = int(25e6/4096/float(freq) -1.0)
        self.sleep()
        self.setRegPrescale(prescale_val)
        time.sleep(0.005)
        self.wakeup()

    def reset(self):
        self.bus.write_byte_data(self.addr, self.__ALL_LED_ON_L, 0)
        self.bus.write_byte_data(self.addr, self.__ALL_LED_ON_H, 0)
        self.bus.write_byte_data(self.addr, self.__ALL_LED_OFF_L, 0)
        self.bus.write_byte_data(self.addr, self.__ALL_LED_OFF_H, 0)
        self.bus.write_byte_data(self.addr, self.__MODE2, 0x04)
        self.bus.write_byte_data(self.addr, self.__MODE1, self.__ALLCALL | self.__AI)
        time.sleep(0.005)

    def chDuty(self, chan, duty):
        if((duty > 100.0)or (duty < 0.0)):
            return
        _off_count = int(4096.0/100.0 * duty)
        self.setValChOff(chan,_off_count)
    def StartHorzion(self,condata):
        if condata <= 140 :
            self.HStartAngle = 70
        if condata >140 and condata <= 270:
            self.HStartAngle = int(75 - abs(condata - 270)/25)
        if condata > 270 and condata < 320:
            self.HStartAngle = int(80 - abs(condata - 320)/9)
        if condata - 320 == 0:
            self.HStartAngle = 85
        if condata > 320 and condata <= 370:
            self.HStartAngle = int(89 + (condata - 320)/9)
        if condata > 370 and condata <= 500:
            self.HStartAngle = int(94 + (condata - 370)/25)
        if condata > 500:
            self.HStartAngle = 100
        val = 180-self.HStartAngle
        angle = (0.05 * 50) + (0.19 * 50 * val / 180)
        self.chDuty(self.Horzionch,angle)
    def StartVertical(self,condata, conflag):
        if conflag == 1:
            if condata - 240 < 0:
                StepDir = 0.2
            elif condata - 240 > 0:
                StepDir = -0.2
            elif condata - 240 == 0:
                StepDir = 0
            self.VStartAngle += StepDir
        if conflag == 0:
            self.VStartAngle += condata
        if self.VStartAngle < 60:
                self.VStartAngle = 60
        if self.VStartAngle > 125:
                self.VStartAngle = 125
        val = 180-self.VStartAngle
        angle = (0.05 * 50) + (0.19 * 50 * val / 180)
        self.chDuty(self.Verticalch,angle)
# VStartAngle 80度為平視, val = 100
# <80 val > 100 往下, > 80 val < 100 往上