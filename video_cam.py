import cv2
import numpy as np
import pyautogui

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

def getFrameStacked(frame1, frame2):
    width, height = pyautogui.size()
    
    w = int(width)
    h = int(height)
        
    frame1 = Rotate(frame1, 270)
    
    alpha = 1280 / 960
    frame1 = cv2.resize(frame1, (int(h / alpha), h))
    frame2 = cv2.resize(frame2, (w - int(h / alpha), h))
    frame = np.hstack((frame1, frame2))

    return frame

def getFrameTexted(frame, text):
    text_location = (25, 25)
    font = cv2.FONT_ITALIC
    scale = 1
    color = (0, 0, 255)
    thick = 2
    line = cv2.LINE_8
    ret = cv2.putText(frame, text, text_location, font, scale, color, thick, line, False)

    return ret

def main():

    cap1 = cv2.VideoCapture('/dev/video0')
    cap2 = cv2.VideoCapture('/dev/video2')

    fps1 = int(cap1.get(cv2.CAP_PROP_FPS))
    fps2 = int(cap2.get(cv2.CAP_PROP_FPS))
    if (fps1 < fps2):
        fps = fps1
    else:
        fps = fps2

    cap1.set(3, 640)
    cap1.set(4, 480)
    cap2.set(3, 640)
    cap2.set(4, 480)

    screen = []
    frame_cnt = 0
    delay_sec = 0
    delay_cnt = int(delay_sec * fps)
    play_cnt = 0

    mode_play = True

    while True:
        if mode_play:
            isNextFrameAvail1, frame1 = cap1.read()
            isNextFrameAvail2, frame2 = cap2.read()
            if not isNextFrameAvail1 or not isNextFrameAvail2:
                print(isNextFrameAvail1)
                print(isNextFrameAvail2)
                break

            frame = getFrameStacked(frame1, frame2)

            curr_time = frame_cnt / fps
            rec_time = curr_time + delay_sec
            # dbgmsg = f'delay {delay_sec} sec, ' + f'current {curr_time:.1f} sec, ' + f'recording {rec_time:.1f} sec'
            dbgmsg = f'delay_sec({delay_sec}), frame_cnt({frame_cnt}), play_cnt({play_cnt})'
            frame = getFrameTexted(frame, dbgmsg)

            screen.append(frame)
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            if frame_cnt > delay_cnt:
                #play_cnt = int(frame_cnt - delay_cnt)
                play_cnt = play_cnt + 1
            else:
                play_cnt = 0
            img = screen[play_cnt]
                
            cv2.imshow('frame', img)
            frame_cnt = frame_cnt + 1

            if (play_cnt > (fps * 10 * 12)):
                # mode_play = False
                screen.clear()
                frame_cnt = 0
                play_cnt = 0
        
        # input handle
        key = cv2.waitKey(1)
        if key & 0xff == ord('q'):
            break
        elif key & 0xff == ord('p'):
            if mode_play:
                mode_play = False
            else:
                mode_play = True
        elif key & 0xff == ord('a'):
            if play_cnt > fps:
                play_cnt = play_cnt - 15
                if mode_play == False:
                    cv2.imshow('frame', screen[play_cnt])
        elif key & 0xff == ord('d'):
            if play_cnt < (frame_cnt - fps):
                play_cnt = play_cnt + 15
                if mode_play == False:
                    cv2.imshow('frame', screen[play_cnt])
        elif key & 0xff == ord('0'):
            delay_sec = 0
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('1'):
            delay_sec = 1
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('2'):
            delay_sec = 2
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('3'):
            delay_sec = 3
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('4'):
            delay_sec = 4
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('5'):
            delay_sec = 5
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('6'):
            delay_sec = 6
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('7'):
            delay_sec = 7
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('8'):
            delay_sec = 8
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
        elif key & 0xff == ord('9'):
            delay_sec = 9
            delay_cnt = int(delay_sec * fps)
            screen.clear()
            frame_cnt = 0
            play_cnt = 0
    
    cap1.release()
    cap2.release()

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
    
