'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
# from flask import Flask, render_template,request
from flask import Flask,render_template, Response, request,abort,jsonify,json
from werkzeug.serving import WSGIRequestHandler
import datetime
import RPi.GPIO as gpio
import time
import cv2
from jing_camera import VideoCamera
from driver_camera_lib import DriverCamera
import urllib.parse

#from FinalCode import helmet
import mcp3008
import PCA9685

#from flask_socketio import SocketIO,emit

try:
    pwms = PCA9685.PCA9685()
    pwms.reset()
    pwms.showInfo()
except:
    print("\x1b[31m",'Warning: PCA9685 Fail!',"\x1b[39m")

wheels_list = ['lf','rf','lb','rb']
switch=0
switch_n=4000
try:
    adc = mcp3008.MCP3008()
except:
    print("mcp3008 is null")
bullet_on=37
Re = 35
bar = 36
#gpio.cleanup() # Release resource
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(Re,gpio.OUT)
gpio.setup(bar,gpio.OUT)
gpio.setup(bullet_on,gpio.OUT)

def setio(p1,p2,p3,p4):
    p = [p1,p2,p3,p4]
    for key in range(0,4):
            index = wheels_list.index(key)
            if int(data[key])>=0 :
                pwms.setValChOff(4*index,0)
                pwms.setValChOff(4*index+2,p[key])
            else:
                pwms.setValChOff(4*index,p[key])
                pwms.setValChOff(4*index+2,0)
pi_camera = VideoCamera(flip=False)
pi_camera.startthread()

driver_camera = DriverCamera(flip=False)
#helmet.InitAll()
time.sleep(1)
app = Flask(__name__)
#cors = CORS(app, resources={r"/video_feed": {'origins': "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=['GET'])
def home():
    now = datetime.datetime.now()
    meth = 'stop'
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
       'title' : 'HELLO!',
       'time': timeString
       } 
    meth=request.args.get('method')
    
    '''global switch
    global switch_n
    if meth == 'switch':
        switch+=1
        if(switch%2==0):
            switch_n=4000
        elif(switch%2==1):
            switch_n=2000
    if meth == 'forward':
        setio(switch_n,switch_n,switch_n,switch_n)
        # 1 1 1 1
    elif meth == 'backward':
        setio(-1*switch_n,-1*switch_n,-1*switch_n,-1*switch_n)
        # -1 -1 -1 -1
    elif meth == 'right':
        setio(-1*switch_n,switch_n,switch_n,-1*switch_n)
        # -1 1 1 -1
    elif meth == 'left':
        setio(switch_n,-1*switch_n,-1*switch_n,switch_n)
        # 1 -1 -1 1
    elif meth == 'turnright':
        setio(-1*switch_n,switch_n,-1*switch_n,switch_n)
        # -1 1 -1 1
    elif meth == 'turnleft':
        setio(switch_n,-1*switch_n,switch_n,-1*switch_n)
        # 1 -1 1 -1'''
    if meth == 'shot':
        gpio.output(Re,False)
        gpio.output(bar,True)
        time.sleep(0.2)
        gpio.output(bar,False)
    elif meth =='re':
        gpio.output(bullet_on,True)
        time.sleep(0.5)
        gpio.output(bullet_on,False)
        gpio.output(Re,True)
    elif meth =='re stop':
        gpio.output(Re,False)
    #volt = adc.diffVolts(2)
    #return render_template("web_mcp.html",volt = volt)
    return render_template("web_mcp.html")


def gen(camera):
  while True:
    frame = camera.show_webcam()
    yield(b'--frame\r\n'
    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/volt', methods=['GET'])
def volt():
 volt = adc.diffVolts(2)
 return str(volt)
@app.route('/video_feed', methods=['GET'])
#@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def video_feed():
  return Response(gen(pi_camera),
     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/driver_video', methods=['GET'])
#@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def driver_video():
  return Response(gen(driver_camera),
     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/wheels', methods=['POST'])
def wheels():
    try:
        data = json.loads(request.form.get('data'))
    except:
        data = request.json
    for key in data.keys():
        index = wheels_list.index(key)
        if int(data[key])>=0 :
            pwms.setValChOff(4*index,0)
            pwms.setValChOff(4*index+2,int(data[key]))
        else:
            pwms.setValChOff(4*index,int(-data[key]))
            pwms.setValChOff(4*index+2,0)
    return '', 200

@app.route('/image_roi', methods=['POST'])
def image_roi():
    data = json.loads(request.form.get('data'))
    #pi_camera.Scale=int(data['Scale'])
    pi_camera.time_count=data['time_count']
    pi_camera.track_sign=data['track_sign']
    return '', 200
@app.route('/tracking_size', methods=['POST'])
def size_adjust():
    data = json.loads(request.form.get('data'))
    pi_camera.ChangeStatus = data['sign']
    return '', 200

@app.route('/Hrotation', methods=['POST'])
def Horizontal_adjust():
    #print(request.args)
    print(request.json)
    data = request.json
    pi_camera.Horziontal = data['horizontal']
    # try:
    #     print(request.form)
    #     data = json.loads(request.form.get('data'))
        
    # except:
    #     return '1 error',202
    '''
    data = request.get_json(force=True)
    print('---2')
    print(data)
    print(data['data'])
    print(data['horizontal'])
    #pi_camera.Horziontal = data['horizontal']
    #print(pi_camera.Horziontal)
    '''
    return '', 200

@app.route('/Vrotation', methods=['POST'])
def Vertical_adjust():
    try:
        print(request.form)
        data = json.loads(request.form.get('vertical'))
        
    except Exception as e:
        return e
    try:
        pi_camera.Vertical = data
    except Exception as ex:
        return ex
    return '', 200


if __name__ == "__main__":
   WSGIRequestHandler.protocol_version = "HTTP/1.1"
   #app.run(host='192.168.1.1', port=8080, debug=False)
   app.run(host='172.24.8.24', port=8080, debug=False)
                                        
'''
('data', '{"horizontal":-1}')
{'horizontal': -1}
-1
'''