import cv2
import numpy as np
import pyautogui
import os

def decideFPS(fps1, fps2):
    if (fps1 < fps2):
        return fps1
    else:
        return fps2
    
def Rotate(src, degrees):
    if degrees == 90:
        dst = cv2.transpose(src)
        dst = cv2.flip(dst, 1)

    elif degrees == 180:
        dst = cv2.flip(dst, -1)

    elif degrees == 270:
        dst = cv2.transpose(src)
        dst = cv2.flip(dst, 0)

    else:
        dst = null

    return dst

def getFrameStacked(f1, f2):
    width, height = pyautogui.size()
    
    w = int(width) #1920
    h = int(height) #1080

    #f1 = f1[0:380, 0:640]
    #f1 = f1[0:640, 0:1280]
    head_w = 1080 # 640 to 1080
    head_h = 610#int(380 *head_w/640) # so 480 to this    
    f1 = cv2.resize(f1, (head_w, head_h))
    f1 = Rotate(f1, 270)

    f2 = f2[0:720 ,100:1180]
    body_w = 1080
    body_h = 720#int(480 *body_w/640)
    f2 = cv2.resize(f2, (body_w, body_h))
    f2 = Rotate(f2, 270)

    # frame = f1
    frame = np.hstack((f1, f2))

    ## translation screen
    # transmatrix = np.array([[1,0,0],[0,1,0]], dtype=np.float32)
    # frame = cv2.warpAffine(src=frame, M=transmatrix, dsize=(1920, 1080))

    # empty_frame = np.zeros((w-head_h-body_h, h, 3), dtype=np.uint8)
    # cv2.putText(empty_frame, userMsg, (25, 25), cv2.FONT_ITALIC, 1, (255,255,255),2,cv2.LINE_8,False)
    # empty_frame = Rotate(empty_frame, 270)
    # frame = np.hstack((frame, empty_frame))

    return frame

class opencv:
    def initCameraDuo(self, path1, path2):
        screen_w, screen_h = pyautogui.size()
        pyautogui.FAILSAFE = False  
        pyautogui.moveTo(screen_w, screen_h)     
        pyautogui.FAILSAFE = True  

        self.cap1 = cv2.VideoCapture(path1, cv2.CAP_V4L2)
        self.cap2 = cv2.VideoCapture(path2, cv2.CAP_V4L2)
        
        self.cap1.set(3, 1280)
        self.cap1.set(4, 720)
        self.cap2.set(3, 1280)
        self.cap2.set(4, 720)
        #self.cap1.set(3, 640)
        #self.cap1.set(4, 480)
        #self.cap2.set(3, 640)
        #self.cap2.set(4, 480)
        # self.cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.cap1.set(cv2.CAP_PROP_FPS, 30)
        self.cap2.set(cv2.CAP_PROP_FPS, 30)
        print(self.cap1.get(cv2.CAP_PROP_FPS))
        print(self.cap2.get(cv2.CAP_PROP_FPS))

        self.fps = decideFPS(int(self.cap1.get(cv2.CAP_PROP_FPS)), int(self.cap2.get(cv2.CAP_PROP_FPS)))
        #self.fps = 30

        return self.fps

    def getFPS(self):
        return self.fps
    
    def getFrameTexted(self, frame, text):
        text_location = (25, 25)
        font = cv2.FONT_ITALIC
        scale = 1
        color = (0, 0, 255)
        thick = 2
        line = cv2.LINE_8
        ret = cv2.putText(frame, text, text_location, font, scale, color, thick, line, False)

        return ret

    def getCameraFrame(self):
        isNextFrameAvail1, frame1 = self.cap1.read()
        isNextFrameAvail2, frame2 = self.cap2.read()

        if not isNextFrameAvail1 or not isNextFrameAvail2:
            print("notNextFrameAvail")
            print(isNextFrameAvail1)
            print(isNextFrameAvail2)
            return 0
        frame = getFrameStacked(frame1, frame2)
        return frame

    def playFrame(self, frame, userMsg):
        screen_w, screen_h = pyautogui.size()

        h = len(frame)
        w = len(frame[0])
        empty_frame = np.zeros((screen_w-w, h, 3), dtype=np.uint8)
        cv2.putText(empty_frame, userMsg, (60, 240), cv2.FONT_ITALIC, 4, (255,255,255),4,cv2.LINE_8,False)
        empty_frame = Rotate(empty_frame, 270)
        frame = np.hstack((frame, empty_frame))

        cv2.namedWindow('frame', cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('frame', frame)

    def waitKey(self, ms):
        key = cv2.waitKey(ms)
        return key
    
    def quit(self):
        try:
            self.cap1.release()
            self.cap2.release()
            cv2.destroyAllWindows()
        except:
            pass

        os.system("shutdown -h now")
