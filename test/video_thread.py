import video
import defines
from multiprocessing import Process, Queue
import time

def recorder(q,ctl):
    v = video.opencv()
    FPS = 0
    FPS = v.initCameraDuo("", "")
    print(FPS)
    if FPS == 0:
        print("init Camera Fail")
        v.quit()
        return
    while ctl.empty():
        f = v.getCameraFrame()
        q.put(f)
    print("stop recording")
    v.quit()

if __name__ == '__main__':
    v = video.opencv()
    mode = defines.MODE()
    frame_queue = Queue()
    control_queue = Queue()

    record_process = Process(target=recorder, args=(frame_queue,control_queue,))
    record_process.start()

    init_frame = frame_queue.get()
    BUFFER = []
    FPS = 30
    play_point = 0
    delay_point = 0
    slow_level = 1
    slow_cnt = 0

    state = mode.IDLE

    while True:
        frame = frame_queue.get()

        if state == mode.PLAY:
            length = len(BUFFER)
            if length >= 5400: # 30 * 180
                del BUFFER[0]
            BUFFER.append(frame)

            if delay_point >= length:
                play_point = 0
                countdown = int((delay_point - length) / FPS) + 1
            else:
                play_point = length - delay_point - 1
                countdown = 0

            msg = f'{(play_point / FPS):5.1f}s ' + f'(x{float(1/(slow_level)):.3f})'
            msg2 = 'Live ' + f'{countdown:5d}'
            v.playFrame(BUFFER[play_point], msg, msg2)
        elif state == mode.REPLAY:
            if slow_cnt % slow_level == 0:
                if play_point < (len(BUFFER) - 1):
                    play_point = play_point + 1
                
                msg = f'{play_point / FPS:5.1f}s ' + f'(x{float(1/(slow_level)):.3f})'
                msg2 = 'Replay'
                v.playFrame(BUFFER[play_point], msg, msg2)
            slow_cnt = slow_cnt + 1
        elif state == mode.STOP:
            msg = f'{play_point / FPS:5.1f}s ' + f'(x{float(1/(slow_level)):.3f})'
            msg2 = 'Replay'
            v.playFrame(BUFFER[play_point], msg, msg2)
        elif state == mode.IDLE:
            msg = f'{play_point / FPS:5.1f}s ' + f'(x{float(1/(slow_level)):.3f})'
            v.playFrame(frame, msg)

        key = v.waitKey(1)
        if key & 0xff == ord('s'):
            if state == mode.STOP or state == mode.REPLAY:
                slow_level = slow_level * 2
                if slow_level > 8:
                    slow_level = 1
        elif key & 0xff == ord('d'):
            state = mode.STOP
            if play_point <= (len(BUFFER) - 15):
                play_point = play_point + 15
        elif key & 0xff == ord('p'):
            if state == mode.PLAY:
                state = mode.STOP
            elif state == mode.REPLAY:
                state = mode.STOP
            elif state == mode.STOP:
                state = mode.REPLAY
        elif key & 0xff == ord('a'):
            state = mode.STOP
            if play_point >= 15:
                play_point = play_point - 15
        elif key & 0xff == ord('r'):
            state = mode.PLAY
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('0'):
            state = mode.IDLE
            delay_point = FPS * 0
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('1'):  
            state = mode.IDLE   
            delay_point = FPS * 1
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('2'):
            state = mode.IDLE
            delay_point = FPS * 2
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('3'):
            state = mode.IDLE
            delay_point = FPS * 3
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('4'):
            state = mode.IDLE
            delay_point = FPS * 4
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('5'):
            state = mode.IDLE
            delay_point = FPS * 5
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('6'):
            state = mode.IDLE
            delay_point = FPS * 6
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('7'):
            state = mode.IDLE
            delay_point = FPS * 7
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('8'):
            state = mode.IDLE
            delay_point = FPS * 8
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('9'):
            state = mode.IDLE
            delay_point = FPS * 9
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        if key & 0xff == ord('q'):
            control_queue.put(key)
            break
    
    time.sleep(1)
    record_process.terminate()
    record_process.join()

    print("shutdown")
