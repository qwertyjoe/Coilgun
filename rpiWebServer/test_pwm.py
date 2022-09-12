import PCA9685

pwms = PCA9685.PCA9685()
pwms.reset()
pwms.showInfo()
pwms.setValChOff(14,50)
pwms.setValChOff(14,00)
# pwms.setValChOff(14+2,int(data[key]))