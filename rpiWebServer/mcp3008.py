import spidev
#import time
#import os
class MCP3008:
  # Open SPI bus
  def __init__(self):
    self.spi = spidev.SpiDev()
    self.spi.open(0,0)
    self.spi.max_speed_hz=1000000

  # Function to read SPI data from MCP3008 chip
  # Channel must be an integer 0-7
  def readChannel(self, channel):
    adc = self.spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data
  # Differential mode
  def readDiff(self, channel):
    adc = self.spi.xfer2([1,(channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data
   
  # Function to convert data to voltage level,
  # rounded to specified number of decimal places.
  def convertVolts(self, data, voltRange = 50, places = 2):
    volts = (data * voltRange) / float(1023)
    volts = round(volts,places)
    return volts

  def diffVolts(self, ch, voltRange = 50):
    return self.convertVolts(self.readDiff(ch), voltRange)

# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
#def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
#  temp = ((data * 330)/float(1023))-50
#  temp = round(temp,places)
#  return temp
 
# Define sensor channels
#light_channel = 2
#temp_channel  = 1
 
# Define delay between readings
#delay = 5
 
#while True:
 
  # Read the light sensor data
#  light_level = ReadChannel(light_channel)
#  light_volts = ConvertVolts(light_level,2)
 
#  # Read the temperature sensor data
#  temp_level = ReadChannel(temp_channel)
#  temp_volts = ConvertVolts(temp_level,2)
#  temp       = ConvertTemp(temp_level,2)
 
  # Print out results
#  print("--------------------------------------------")
#  print("Light: {} ({}V)".format(light_level,light_volts))
#  print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
 
  # Wait before repeating loop
#  time.sleep(1)
