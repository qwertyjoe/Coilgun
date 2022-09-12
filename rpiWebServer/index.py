from flask import Flask,render_template, Response, request,abort,jsonify,json
from werkzeug.serving import WSGIRequestHandler
import datetime
import RPi.GPIO as gpio
import time
import cv2
from jing_camera import VideoCamera
from driver_camera_lib import DriverCamera
import urllib.parse
import CAMstepper
import threading, queue
import sys
import glob
import math
import traceback

from gevent import monkey

from gevent.pywsgi import WSGIServer

pi_camera = VideoCamera(flip=False)
driver_camera = DriverCamera(flip=False)
pi_camera.startthread()

CamPath = '/dev/video*'
video_files = None
pwms = None
tf = None
adc = None
message = ""
Horizontal_Ch = None

def CamNum():
    global video_files
    video_files = glob.glob(CamPath)
    for i,file in enumerate(video_files[::-1]):
        video_files[i] = file[10:]
    camera_all_reset(video_files)
    print(video_files)

def PCA9685_start():
    try:
        import PCA9685
        import ServoGpio
        global pwms, servo_pca, Horizontal_Ch
        servo_pca = None
        pwms = None
        time.sleep(0.5)
        servo_pca = ServoGpio.PCA9685()
        Horizontal_Ch = servo_pca.Horzionch
        pwms = PCA9685.PCA9685()
        pwms.reset()
        pwms.showInfo()
        pi_camera.ServoStepper = ServoGpio.PCA9685()
    except Exception as e:
        print("\x1b[31m",'Warning: PCA9685 Fail!',"\x1b[39m")
        print(repr(e))

def tfmini_start():
    try:
        import tfmini
        global tf
        tf = tfmini.tfmini()
    except Exception as e:
        print("\x1b[31m",'Warning: MiniToF Fail!',"\x1b[39m")
        print(repr(e))

def mcp3008_start():
    try:
        import mcp3008
        global adc
        adc = mcp3008.MCP3008()
    except Exception as e:
        print("\x1b[31m",'Warning: MCP3008 Fail!',"\x1b[39m")
        print(repr(e))
        traceback.print_exc()

wheels_list = ['lf','rf','lb','rb']
switch=0
switch_n=4000
bullet_on=33 #37
#Re = 31 #35
Re = 31
bar = 36
#gpio.cleanup() # Release resource
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(Re,gpio.OUT)
gpio.setup(bar,gpio.OUT)
gpio.setup(bullet_on,gpio.OUT)
gpio.output(bullet_on,True)

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

def camera_all_reset(VideoPath):
    try:
        pi_camera.cam = None
        driver_camera.cam = None
        time.sleep(0.2)
        pi_camera.camera_reset(int(VideoPath[0]))
        driver_camera.camera_reset(int(VideoPath[1]))
    except:
        print(sys.exc_info())
def camera_start(value):
    if value == 1:
        pi_camera.cam = None
        time.sleep(0.5)
        pi_camera.camera_reset(int(video_files[0]))
    if value == 2:
        driver_camera.cam = None
        time.sleep(0.5)
        driver_camera.camera_reset(int(video_files[1]))
def camera_switch():
    global video_files
    size = len(video_files)
    if size == 1:
        CamNum()
        size = len(video_files)
    print('switch start')
    if size == 2:
        pi_camera.cam = None
        driver_camera.cam = None
        temp = video_files[0]
        video_files[0] = video_files[1]
        video_files[1] = temp
        pi_camera.camera_reset(int(video_files[0]))
        driver_camera.camera_reset(int(video_files[1]))
        print('switch complete')
def AutoShot():
    global tf,servo_pca
    #data = request.json()
    distance = tf.getdistance()
    G = 980
    V = 158
    UP = 0.0
    Down = 0.0
    # from ToF and y to calculate x
    print("distance:",distance)
    print("Start Angle:",pi_camera.ServoStepper.VStartAngle)
    x = math.cos(math.radians(abs(pi_camera.ServoStepper.VStartAngle - 80))) * distance
    y = math.sin(math.radians(abs(pi_camera.ServoStepper.VStartAngle - 80))) * distance
    print("X=",x," Y=",y)
    try:
        V_Pow_2 = math.pow(V,2)
        print("V_Pow_2=",V_Pow_2)
        V_Pow_4 = math.pow(V,4)
        print("V_Pow_4=",V_Pow_4)
        G_Pow_2 = math.pow(G,2)
        print("G_Pow_2=",G_Pow_2)
        x_Pow_2 = math.pow(x,2)
        print("x_Pow_2=",x_Pow_2)
        if ( (V_Pow_4 >= (2*G*V_Pow_2*y+G_Pow_2*x_Pow_2)) and not(x == 0)):
            print("Here")
            print("Cal:",V_Pow_4-2*G*V_Pow_2*y-G_Pow_2*x_Pow_2)
            Sqrt_ans = math.sqrt(V_Pow_4-2*G*V_Pow_2*y-G_Pow_2*x_Pow_2) / (G*x)
            print("Sqrt_ans=",Sqrt_ans)
            Up = math.atan(math.radians(( V_Pow_2 / (G*x)) ) + Sqrt_ans)
            print("Up=",Up)
            Down = math.atan(math.radians( V_Pow_2 / (G*x) ) - Sqrt_ans)
            print("Down=",Down)
            FinalAngle = 0.0
            print("FinalAngle")
            if UP <= 90 and Up >= 0 :
                FinalAngle = UP + 80
                pi_camera.ServoStepper.chDuty(1,FinalAngle)
                print("Up")
            elif Down <= 90 and Down >= 0 :
                FinalAngle = Down + 80
                pi_camera.ServoStepper.chDuty(1,FinalAngle)
                print("Down")
            else:
                print("超出範圍")
        else:
            print("靠北")
    except Exception as e:
        print(e.message)


app = Flask(__name__)
#cors = CORS(app, resources={r"/video_feed": {'origins': "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'
ManualShotFlag = 0
@app.route('/',methods=['GET'])
def home():
    global pi_camera
    global ManualShotFlag
    now = datetime.datetime.now()
    meth = 'stop'
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
       'title' : 'HELLO!',
       'time': timeString
       } 
    meth = request.args.get('method')
    
    if meth == 'shot':
        #pi_camera.ManualShotFlag = 1
        #ManualShotFlag = 1
        #AutoShot()
        #time.sleep(1)
        gpio.output(Re,False)
        gpio.output(bar,True)
        time.sleep(0.2)
        #gpio.output(bar,False)
    elif meth == 're':
        gpio.output(bullet_on,False)
        time.sleep(0.2)
        gpio.output(bullet_on,True)
        gpio.output(Re,True)
    elif meth == 're stop':
        gpio.output(Re,False)
        gpio.output(bullet_on,True)
        gpio.output(bar,False)
    #volt = adc.diffVolts(2)
    #return render_template("web_mcp.html",volt = volt)
    return render_template("web_mcp.html")

@app.route('/sec',methods=['GET'])
def SecHome():
    return render_template("sec_web.html")

def SecGen(camera):
    while True:
        frame = camera.show_webcam()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen(camera):
    while True:
        frame = camera.show_webcam()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/info', methods=['GET'])
def info():
    # volt /48.5*50 
    m_info = {"volt":-1,"message":"Start Init Accel Gyro"}
    try:
        m_info["volt"] = adc.diffVolts(2)/48.5*50
    except:
        m_info["volt"]=-1
    m_info["message"] = message
    return m_info

@app.route('/volt', methods=['GET'])
def volt():
    m_info = {"volt":-1,"message":"Start Init Accel Gyro"}
    try:
        m_info["volt"] = float(adc.diffVolts(2))/48.5*50
    except:
        m_info["volt"] = -1
    return str(m_info["volt"])

@app.route('/video_feed', methods=['GET'])
#@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def video_feed():
    return Response(gen(pi_camera),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/driver_video', methods=['GET'])
#@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def driver_video():
    return Response(SecGen(driver_camera),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/wheels', methods=['POST'])
def wheels():
    try:
        data = json.loads(request.form.get('data'))
    except:
        data = request.json
    print(data)
    for key in data.keys():
        index = wheels_list.index(key)
        if int(data[key])>=0 :
            pwms.setValChOff(4*index,0)
            pwms.setValChOff(4*index+2,int(data[key]))
        else:
            pwms.setValChOff(4*index,int(-data[key]))
            pwms.setValChOff(4*index+2,0)
    return '', 200
track_sign = 0
@app.route('/image_roi', methods=['POST'])
def image_roi():
    global track_sign
    try:
        data = json.loads(request.form.get('data'))
    except:
        data = request.json
    pi_camera.time_count=data['time_count']
    pi_camera.track_sign=data['track_sign']
    track_sign = data['track_sign']
    Horizontal_detect()
    return '', 200

@app.route('/tracking_size', methods=['POST'])
def size_adjust():
    try:
        data = json.loads(request.form.get('data'))
    except:
        data = request.json
    pi_camera.ChangeStatus = data['sign']
    return '', 200

Horizontal_Angle = 85
@app.route('/Hrotation', methods=['POST'])
def Horizontal_adjust():
    global Horizontal_Angle
    data = request.json
    Horizontal_Angle = data['horizontal']
    Horizontal_detect()
    return '', 200

CurrentSign = 0
def Horizontal_detect():
    global Horizontal_Angle
    global CurrentSign
    global ManualShotFlag
    if ManualShotFlag == 0:
        if track_sign == 0 :
            if CurrentSign == 1:
                CurrentSign = 0
                Horizontal_Angle = 85
            val = 180-Horizontal_Angle
            angle = (0.05 * 50) + (0.19 * 50 * val / 180)
            servo_pca.chDuty(Horizontal_Ch,angle)
        if track_sign == 1:
            CurrentSign = 1
    else:
        time.sleep(1.2)
        ManualShotFlag = 0


@app.route('/Vrotation', methods=['POST'])
def Vertical_adjust():
    global VerticalDirection
    data = request.json
    pi_camera.Vertical = data['vertical']
    return '', 200

@app.route('/Rotation', methods=['POST'])
def Roatation_adjust():
    global Horizontal_Angle
    data = request.json
    pi_camera.Vertical = data['vertical']
    Horizontal_Angle = data['horizontal']
    Horizontal_detect()
    print("Var : ",data['vertical'])
    print("Hor : ",data['horizontal'])
    return '', 200


@app.route('/InitMPU',methods=['POST'])
def Init_MPU():
    data = request.json
    global message
    message = data['message']
    return '',200

@app.route('/Setting', methods=['POST'])
def Setting():
    data = request.json
    value = data['setting']
    if value == 'pi_cam':
        camera_start(1)
    if value == 'driver_cam':
        camera_start(2)
    if value == 'cam_index':
        CamNum()
    if value == 'cam_switch':
        camera_switch()
    if value == 'reset_modules':
        PCA9685_start()
        tfmini_start()
        mcp3008_start()
    return '',200
def get_command():
    while True:
        command = input()
        if command == "PCA9685" or command == "PCA":
            print("restarting PCA")
            PCA9685_start()
        if command == "minitf":
            tfmini_start()
        if command == "mcp3008" or command == "mcp":
            mcp3008_start()
        if command == "cam1":
            camera_start(1)
        if command == "cam2":
            camera_start(2)
        if command == "camre":
            CamNum()
        if command == "camsw":
            camera_switch()
            
#get_command_thread = threading.Thread(target=app.run(host='192.168.1.1', port=8080, debug=False))
#get_command_thread.start()
WSGIRequestHandler.protocol_version = "HTTP/1.1"
print('starting')
CamNum()
print('cam running')
PCA9685_start()
tfmini_start()
mcp3008_start()
get_command_thread = threading.Thread(target=get_command)
get_command_thread.start()
# print('get comd')
if __name__ == "__main__":
    print('server starting')
    
    # meinheld.listen(('192.168.1.1', 8080))
    # meinheld.run(app)

    # monkey.patch_all()
    # server = WSGIServer(('192.168.1.1',8080), app)
    # server.serve_forever()
    #app.run(host='192.168.1.1', port=8080, debug=False)
    app.run(host='0.0.0.0', port=8080, debug=False)
    print('server stop')
    
