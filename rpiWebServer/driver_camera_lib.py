import cv2
import time


class DriverCamera(object):
    def __init__(self, flip = False):
        self.CamNum = 1
        self.cam = cv2.VideoCapture(self.CamNum)
        self.cam.set(cv2.CAP_PROP_FPS, 30)
        self.StartFrameTime = 0
        self.PrevFrameTime = 0
    def camera_reset(self,num):
        self.cam = None
        self.CamNum = num
        time.sleep(0.1)
        self.cam = cv2.VideoCapture(self.CamNum)
        self.cam.set(cv2.CAP_PROP_FPS, 30)
    def show_webcam(self):
        while True:
            self.StartFrameTime = time.time()
            ret_val, img = self.cam.read()
            fps = 1/(self.StartFrameTime - self.PrevFrameTime)
            self.PrevFrameTime = self.StartFrameTime
            fps = int(fps)
            fps = str(fps)
            cv2.putText(img, fps, (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
            rect,jpeg = cv2.imencode('.jpg',img)
            return jpeg.tobytes()
