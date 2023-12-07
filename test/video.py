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

    # f2 = f2[0:720 ,100:1180]
    body_w = 1080
    # body_h = 720#int(480 *body_w/640)
    body_h = 610
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
    IMG1_LIVEMODE = cv2.imread('img/LIVEMODE.png')
    IMG1_REVIEWMODE = cv2.imread('img/REVIEWMODE.png')
    IMG2_X10 = cv2.imread('img/X10.png')
    IMG2_X05 = cv2.imread('img/X05.png')
    IMG2_X025 = cv2.imread('img/X025.png')
    IMG2_X012 = cv2.imread('img/X012.png')
    IMG3_PLAY = cv2.imread('img/PLAY.png')
    IMG3_PAUSE = cv2.imread('img/PAUSE.png')
    IMG3_READY = cv2.imread('img/READY.png')
    IMG3_REPLAY = cv2.imread('img/REPLAY.png')
    IMG3_FF = cv2.imread('img/FF.png')
    IMG3_REW = cv2.imread('img/REW.png')
    IMG3 = [IMG3_READY, IMG3_PLAY, IMG3_REPLAY, IMG3_PAUSE, IMG3_FF, IMG3_REW]

    def initCameraDuo(self, path1, path2):
        screen_w, screen_h = pyautogui.size()
        pyautogui.FAILSAFE = False  
        pyautogui.moveTo(screen_w, screen_h)     
        pyautogui.FAILSAFE = True  

        self.cap1 = cv2.VideoCapture(path1, cv2.CAP_V4L2)
        self.cap2 = cv2.VideoCapture(path2, cv2.CAP_V4L2)
        # self.cap1 = cv2.VideoCapture(0)
        # self.cap2 = cv2.VideoCapture(1)
        
        self.cap1.set(3, 1280)
        self.cap1.set(4, 720)
        self.cap2.set(3, 1280)
        self.cap2.set(4, 720)
        # self.cap1.set(3, 640)
        # self.cap1.set(4, 480)
        # self.cap2.set(3, 640)
        # self.cap2.set(4, 480)
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

        self.cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap2.set(cv2.CAP_PROP_BUFFERSIZE, 1)

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
        # isNextFrameAvail1 = isNextFrameAvail2
        # frame1 = frame2

        if not isNextFrameAvail1 or not isNextFrameAvail2:
            print("notNextFrameAvail")
            print(isNextFrameAvail1)
            print(isNextFrameAvail2)
            return 0
        frame = getFrameStacked(frame1, frame2)
        return frame

    def playFrame(self, frame, userMsg = "", userMsg2 = "", mode = 0, slow = 1, status = 0):
        screen_w, screen_h = pyautogui.size()

        h = len(frame)
        w = len(frame[0])
        empty_frame = np.zeros((screen_w-w, h, 3), dtype=np.uint8)
        position1 = (25, 25)
        area1 = (1030, 115)
        if mode == 0:
            img1 = cv2.resize(self.IMG1_LIVEMODE, area1)
        else:
            img1 = cv2.resize(self.IMG1_REVIEWMODE, area1)
        empty_frame[position1[1]:position1[1]+len(img1), position1[0]:position1[0]+len(img1[0])] = img1
        
        position2 = (565, 215)
        area2 = (400, 96)
        if slow == 1:
            img2 = cv2.resize(self.IMG2_X10, area2)
        elif slow == 2:
            img2 = cv2.resize(self.IMG2_X05, area2)
        elif slow == 4:
            img2 = cv2.resize(self.IMG2_X025, area2)
        elif slow == 8:
            img2 = cv2.resize(self.IMG2_X012, area2)
        empty_frame[position2[1]:position2[1]+len(img2), position2[0]:position2[0]+len(img2[0])] = img2

        position3 = (262, 350)
        area3 = (555, 174)
        img3 = cv2.resize(self.IMG3[status], area3)

        empty_frame[position3[1]:position3[1]+len(img3), position3[0]:position3[0]+len(img3[0])] = img3

        cv2.putText(empty_frame, userMsg, (60, 290), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255),4,cv2.FILLED,False)
        cv2.putText(empty_frame, userMsg2, (60, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255),4,cv2.FILLED,False)

        empty_frame = Rotate(empty_frame, 270)
        frame = np.hstack((frame, empty_frame))

        cv2.namedWindow('frame', cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('frame', frame)

    def Record(self, buf):
        try:
            width, height = buf[0].shape[:2]
            frame_size = (width, height)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('/home/donnyunn/Desktop/LastRecord.mp4',fourcc,30.0,frame_size)
            for frame in buf:
                frame = cv2.transpose(frame)
                frame = cv2.flip(frame, 1)
                out.write(frame)
            out.release()
        except:
            pass

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
