import video
import defines
from multiprocessing import Process, Queue
import time
from datetime import datetime
import pyudev

def find_all_usb_webcam_paths():
    context = pyudev.Context()
    webcam_paths = []

    for device in context.list_devices(subsystem='video4linux'):
        # USB 웹캠 장치를 찾음
        if device.sys_name.startswith("video"):
            webcam_paths.append(device.device_node)

    return webcam_paths

def recorder(q,ctl):
    v = video.opencv()

    webcam_paths = find_all_usb_webcam_paths()
    print(webcam_paths)

    FPS = 0
    FPS = v.initCameraDuo(webcam_paths[2], webcam_paths[0])
    print(FPS)
    f = v.getCameraFrame()
    if FPS == 0:
        print("init Camera Fail")
        v.quit()
        return
    while ctl.empty():
        try:
            f = v.getCameraFrame()
            q.put(f)
        except:
            pass
    print("stop recording")
    v.quit()

def write_worker(v, buffer):
    v.Record(buffer)

def writer(v, buffer):
    write_process = Process(target=write_worker, args=(v,buffer,))
    write_process.start()

def log(msg):
    now = datetime.now()
    logtime = now.strftime("%Y-%m-%d_%H:%M:%S")
    print(f'{logtime} > {msg}')

if __name__ == '__main__':
    FPS = 30
    BUFFER = []

    time.sleep(1)

    v = video.opencv()
    mode = defines.MODE()
    frame_queue = Queue(5671)
    control_queue = Queue()

    record_process = Process(target=recorder, args=(frame_queue,control_queue,))
    record_process.start()

    init_frame = frame_queue.get()
    end_point = FPS * 180
    play_point = 0
    delay_point = 0
    slow_level = 1
    slow_cnt = 0
    blackbox_cnt = 0

    state = mode.IDLE
    log('Starting the program [Idle]')
    # state = mode.PLAY

    while True:
        frame = frame_queue.get()

        if state == mode.PLAY:
            length = len(BUFFER)
            if length >= (end_point + delay_point): # 30 * 180
                del BUFFER[0]
            BUFFER.append(frame)
            blackbox_cnt = blackbox_cnt + 1
            if blackbox_cnt >= 1800:
                log(f'Saving Automatically.. ({len(BUFFER)-blackbox_cnt}:{len(BUFFER)-1})')
                writer(v, BUFFER[len(BUFFER)-blackbox_cnt:len(BUFFER)-1])
                blackbox_cnt = 0

            if delay_point >= length:
                play_point = 0
                countdown = int((delay_point - length - 1) / FPS) + 1
            else:
                play_point = length - delay_point - 1
                countdown = 0

            msg = f'{(play_point / FPS):5.1f}s'
            if countdown != 0:
                msg2 = f'{countdown:5d}'
            else:
                msg2 = ""
            v.playFrame(BUFFER[play_point], msg, msg2, state, 1, 1)
        elif state == mode.REPLAY:
            if slow_cnt % slow_level == 0:
                if play_point < (len(BUFFER) - 1):
                    play_point = play_point + 1
                else:
                    state = mode.STOP
                    log('Frame end [Pause]')
                
                msg = f'{play_point / FPS:5.1f}s'
                msg2 = ""
                v.playFrame(BUFFER[play_point], msg, msg2, state, slow_level, 2)
            slow_cnt = slow_cnt + 1
        elif state == mode.STOP:
            status = 3
            if key & 0xff == ord('d'):
                status = 4
            elif key & 0xff == ord('a'):
                status = 5
            msg = f'{play_point / FPS:5.1f}s'
            msg2 = ""
            v.playFrame(BUFFER[play_point], msg, msg2, state, slow_level, status)
            status = 3
        elif state == mode.IDLE:
            msg = f'{play_point / FPS:5.1f}s'
            v.playFrame(frame, msg)

        key = v.waitKey(1)
        if key & 0xff == ord('s'):
            if state == mode.STOP or state == mode.REPLAY:
                slow_level = slow_level * 2
                if slow_level > 8:
                    slow_level = 1                
                log(f'Key pressed [Slow (1/{slow_level})]')
        elif key & 0xff == ord('d'):
            if state != mode.IDLE:
                state = mode.STOP
                log('Key pressed [FF]')
                if play_point <= (len(BUFFER) - 15):
                    play_point = play_point + 15
        elif key & 0xff == ord('p'):
            if state == mode.PLAY:
                state = mode.STOP    
                log('Key pressed [Pause]')
            elif state == mode.REPLAY:
                state = mode.STOP
                log('Key pressed [Pause]')
            elif state == mode.STOP:
                state = mode.REPLAY
                log('Key pressed [Replay]')
        elif key & 0xff == ord('a'):
            if state != mode.IDLE:
                state = mode.STOP
                log('Key pressed [REW]')
                if play_point >= 15:
                    play_point = play_point - 15                
        elif key & 0xff == ord('r'):
            if state == mode.IDLE:
                state = mode.PLAY                
                log('Key pressed [Record]')
            else:
                state = mode.IDLE
                log('Key pressed [Idle]')
                if blackbox_cnt != 0:
                    log(f'Saving Manually.. ({len(BUFFER)-blackbox_cnt}:{len(BUFFER)-1})')
                    writer(v, BUFFER[len(BUFFER)-blackbox_cnt:len(BUFFER)-1])
                    blackbox_cnt = 0
                
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('0'):
            state = mode.IDLE
            log('Key pressed [0]')
            delay_point = FPS * 0
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('1'):  
            state = mode.IDLE   
            log('Key pressed [1]')
            delay_point = FPS * 1
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('2'):
            state = mode.IDLE
            log('Key pressed [2]')
            delay_point = FPS * 2
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('3'):
            state = mode.IDLE
            log('Key pressed [3]')
            delay_point = FPS * 3
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('4'):
            state = mode.IDLE
            log('Key pressed [4]')
            delay_point = FPS * 4
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('5'):
            state = mode.IDLE
            log('Key pressed [5]')
            delay_point = FPS * 5
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('6'):
            state = mode.IDLE
            log('Key pressed [6]')
            delay_point = FPS * 6
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('7'):
            state = mode.IDLE
            log('Key pressed [7]')
            delay_point = FPS * 7
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('8'):
            state = mode.IDLE
            log('Key pressed [8]')
            delay_point = FPS * 8
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('9'):
            state = mode.IDLE
            log('Key pressed [9]')
            delay_point = FPS * 9
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        if key & 0xff == ord('q'):
            log('Key pressed [Power off]')
            control_queue.put(key)
            break

    time.sleep(1)
    record_process.terminate()
    record_process.join()

