
'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
from flask import Flask, render_template,request
import datetime
import RPi.GPIO as gpio
import time
import mcp3008
from flask import Flask,render_template, Response, request,abort,jsonify,json
#from flask_socketio import SocketIO,emit
from jing_camera import VideoCamera
import cv2
from flask_cors import CORS, cross_origin

adc = mcp3008.MCP3008()
RFWa = 11
RFWb = 12
LFWa = 13
LFWb = 15
RBWa = 16
RBWb = 18
LBWa = 29
LBWb = 31
Re = 33
bar = 35
bullet_on=36
#gpio.cleanup() # Release resource
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(RFWa,gpio.OUT)
gpio.setup(RFWb,gpio.OUT)
gpio.setup(LFWa,gpio.OUT)
gpio.setup(LFWb,gpio.OUT)
gpio.setup(RBWa,gpio.OUT)
gpio.setup(RBWb,gpio.OUT)
gpio.setup(LBWa,gpio.OUT)
gpio.setup(LBWb,gpio.OUT)
gpio.setup(Re,gpio.OUT)
gpio.setup(bar,gpio.OUT)
gpio.setup(bullet_on,gpio.OUT)
def setio(p1,p2,p3,p4,p5,p6,p7,p8):
    gpio.output(RFWa,p1)
    gpio.output(RFWb,p2)
    gpio.output(LFWa,p3)
    gpio.output(LFWb,p4)
    gpio.output(RBWa,p5)
    gpio.output(RBWb,p6)
    gpio.output(LBWa,p7)
    gpio.output(LBWb,p8)

pi_camera = VideoCamera(flip=False)
app = Flask(__name__)
cors = CORS(app, resources={r"/video_feed": {'origins': "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=['GET'])
def home():
    now = datetime.datetime.now()
    meth = 'stop'
    timeString = now.strftime("%Y-%m-%d %H:%M")
    meth=request.args.get('method')
    
    if meth == 'forward':
        setio(True,False,True,False,True,False,True,False)
    elif meth == 'backward':
        setio(False,True,False,True,False,True,False,True)
    elif meth == 'right':
        setio(False,True,True,False,True,False,False,True)
    elif meth == 'left':
        setio(True,False,False,True,False,True,True,False)
    elif meth == 'turnright':
        setio(False,True,True,False,False,True,True,False)
    elif meth == 'turnleft':
        setio(True,False,False,True,True,False,False,True)
    elif meth == 'stop':
        setio(False,False,False,False,False,False,False,False)
    if meth == 'shot':
        gpio.output(bar,True)
        time.sleep(0.1)
        gpio.output(bar,False)
    elif meth =='re':
        gpio.output(bullet_on,True)
        time.sleep(0.5)
        gpio.output(bullet_on,False)
        gpio.output(Re,True)
    elif meth =='re stop':
        gpio.output(Re,False)
    volt = adc.diffVolts(2)
    return render_template("web_mcp.html", volt = volt)

def gen(camera):
  while True:
    frame = camera.Rectangle()
    yield(b'--frame\r\n'
    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/volt')
def volt():
  volt = adc.diffVolts(2)
  return str(volt)

@app.route('/video_feed', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def video_feed():
  return Response(gen(pi_camera),
     mimetype='multipart/x-mixed-replace; boundary=frame',
     headers='')

@app.route('/image_roi', methods=['POST'])
def image_roi():
    data = json.loads(request.form.get('data'))
    pi_camera.x=int(data['x'])
    pi_camera.y=int(data['y'])
    pi_camera.Scale=int(data['Scale'])
    pi_camera.time_count=data['time_count']
    pi_camera.track_sign=data['track_sign']
    return '', 200

if __name__ == "__main__":
   app.run(host='172.24.8.23', port=8080, debug=False)
                                        
