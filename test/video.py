import cv2
import numpy as np
import pyautogui

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
    
    w = int(width)
    h = int(height)
        
    # f1 = Rotate(f1, 270)
    
    # alpha = 1280 / 960
    # f1 = cv2.resize(f1, (int(h / alpha), h))
    # f2 = cv2.resize(f2, (w - int(h / alpha), h))
    # frame = np.hstack((f1, f2))

    f1 = f1[100:380, 0:640]
    f1 = cv2.resize(f1, (1080, 480))
    f1 = Rotate(f1, 270)

    f2 = f2[0:480 ,140:500]
    f2 = cv2.resize(f2, (1080, 1440))
    f2 = Rotate(f2, 270)

    # frame = f1
    frame = np.hstack((f1, f2))

    return frame

class opencv:
    def initCameraDuo(self, path1, path2):
        self.cap1 = cv2.VideoCapture(path1)
        self.cap2 = cv2.VideoCapture(path2)

        self.fps = decideFPS(int(self.cap1.get(cv2.CAP_PROP_FPS)), int(self.cap2.get(cv2.CAP_PROP_FPS)))

        self.cap1.set(3, 640)
        self.cap1.set(4, 480)
        self.cap2.set(3, 640)
        self.cap2.set(4, 480)

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
            return 0
        frame = getFrameStacked(frame1, frame2)
        return frame

    def playFrame(self, frame):
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('frame', frame)

    def waitKey(self, ms):
        key = cv2.waitKey(ms)
        return key
    
    def quit(self):
        self.cap1.release()
        self.cap2.release()
        cv2.destroyAllWindows()