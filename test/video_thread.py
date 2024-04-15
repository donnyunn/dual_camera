import video
import defines
from multiprocessing import Process, Queue, Pipe
import time
from datetime import datetime
import pyudev
import os
from threading import Timer

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

def deleter_worker(p, result):
    p.send(['',(0,0,0), result[2]])

def write_worker(v, buffer,p):
    p.send(["File Writing", (0,0,255), 0])
    result = v.Record(buffer)
    p.send([result[0], result[1], result[2]])
    Timer(10, deleter_worker, args=(p, result)).start()
    # time.sleep(10)
    # p.send(['',(0,0,0), result[2]])

def writer(v, buffer, pipe):
    write_process = Process(target=write_worker, args=(v,buffer,pipe,))
    write_process.start()

def log(msg):
    now = datetime.now()
    logtime = now.strftime("%Y-%m-%d_%H:%M:%S")
    print(f'{logtime} [{msg}]')

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
    blackbox_onoff = 0
    blackbox_r, blackbox_s = Pipe()
    blackbox_path = ''
    blackbox_usb = 0
    blackbox = ['',(0,0,0),blackbox_path]

    try:
        base_path = '/media'
        subdirectories = v.get_all_subdirectories(base_path)
        if subdirectories:
            if os.path.isdir(subdirectories[1]):
                blackbox_usb = 1
                # print(subdirectories[1])
    except:
        blackbox_usb = 0

    state = mode.IDLE
    log('Device ON (Idle)')
    # state = mode.PLAY

    while True:
        frame = frame_queue.get()
        
        if blackbox_r.poll():
            blackbox = blackbox_r.recv()
            blackbox_path = blackbox[2]

        if state == mode.PLAY:
            length = len(BUFFER)
            if length >= (end_point + delay_point): # 30 * 180
                del BUFFER[0]
            BUFFER.append(frame)
            if blackbox_onoff == 1:
                blackbox_cnt = blackbox_cnt + 1
                if blackbox_cnt >= 1800:
                    log(f'Saving Automatically.. ({len(BUFFER)-blackbox_cnt}:{len(BUFFER)-1})')
                    writer(v, BUFFER[len(BUFFER)-blackbox_cnt:len(BUFFER)-1], blackbox_s)
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
            v.playFrame(BUFFER[play_point], blackbox_onoff, msg, msg2, state, 1, 1, blackbox[0], blackbox[1])
        elif state == mode.REPLAY:
            if slow_cnt % slow_level == 0:
                if play_point < (len(BUFFER) - 1):
                    play_point = play_point + 1
                else:
                    state = mode.STOP
                    log('Frame end [Pause]')
                
                msg = f'{play_point / FPS:5.1f}s'
                msg2 = ""
                v.playFrame(BUFFER[play_point], blackbox_onoff, msg, msg2, state, slow_level, 2, blackbox[0], blackbox[1])
            slow_cnt = slow_cnt + 1
        elif state == mode.STOP:
            status = 3
            if key & 0xff == ord('d'):
                status = 4
            elif key & 0xff == ord('a'):
                status = 5
            msg = f'{play_point / FPS:5.1f}s'
            msg2 = ""
            v.playFrame(BUFFER[play_point], blackbox_onoff, msg, msg2, state, slow_level, status, blackbox[0], blackbox[1])
            status = 3
        elif state == mode.IDLE:
            msg = f'{play_point / FPS:5.1f}s'
            v.playFrame(frame, blackbox_onoff, msg, bbMsg=blackbox[0], bbMsgColor=blackbox[1])

        key = v.waitKey(1)
        if key & 0xff == ord('s'):
            if state == mode.STOP or state == mode.REPLAY:
                slow_level = slow_level * 2
                if slow_level > 8:
                    slow_level = 1                
                log(f'Key pressed Slow (1/{slow_level})')
            elif state == mode.IDLE:
                if blackbox_onoff == 0:
                    blackbox_onoff = 1
                else:
                    blackbox_onoff = 0
                log(f'Key pressed Blackbox ({blackbox_onoff})')
        elif key & 0xff == ord('d'):
            if state != mode.IDLE:
                state = mode.STOP
                log('Key pressed FF')
                if play_point <= (len(BUFFER) - 15):
                    play_point = play_point + 15
        elif key & 0xff == ord('p'):
            if state == mode.PLAY:
                state = mode.STOP    
                log('Key pressed Pause')
            elif state == mode.REPLAY:
                state = mode.STOP
                log('Key pressed Pause')
            elif state == mode.STOP:
                state = mode.REPLAY
                log('Key pressed Replay')
        elif key & 0xff == ord('a'):
            if state != mode.IDLE:
                state = mode.STOP
                log('Key pressed REW')
                if play_point >= 15:
                    play_point = play_point - 15                
        elif key & 0xff == ord('r'):
            if state == mode.IDLE:
                state = mode.PLAY                
                # log('Key pressed Record')
                if blackbox_onoff == 0:
                    save = 'SAVE OFF'
                else:
                    save = 'SAVE ON'
                if blackbox_usb == 0:
                    usb = 'HDD'
                else:
                    usb = 'USB'
                log(f'PLAY ON:{save}:{usb}')
            else:
                state = mode.IDLE
                # log('Key pressed Ready')
                if blackbox_onoff == 1:
                    if blackbox_cnt != 0:
                        # log(f'Saving Manually.. ({len(BUFFER)-blackbox_cnt}:{len(BUFFER)-1})')
                        writer(v, BUFFER[len(BUFFER)-blackbox_cnt:len(BUFFER)-1], blackbox_s)
                        blackbox_cnt = 0
                
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('0'):
            state = mode.IDLE
            log('Key pressed 0')
            delay_point = FPS * 0
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('1'):  
            state = mode.IDLE   
            log('Key pressed 1')
            delay_point = FPS * 1
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('2'):
            state = mode.IDLE
            log('Key pressed 2')
            delay_point = FPS * 2
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('3'):
            state = mode.IDLE
            log('Key pressed 3')
            delay_point = FPS * 3
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('4'):
            state = mode.IDLE
            log('Key pressed 4')
            delay_point = FPS * 4
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('5'):
            state = mode.IDLE
            log('Key pressed 5')
            delay_point = FPS * 5
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('6'):
            state = mode.IDLE
            log('Key pressed 6')
            delay_point = FPS * 6
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('7'):
            state = mode.IDLE
            log('Key pressed 7')
            delay_point = FPS * 7
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('8'):
            state = mode.IDLE
            log('Key pressed 8')
            delay_point = FPS * 8
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        elif key & 0xff == ord('9'):
            state = mode.IDLE
            log('Key pressed 9')
            delay_point = FPS * 9
            play_point = 0
            slow_level = 1
            BUFFER.clear()
        if key & 0xff == ord('q'):
            log('Device OFF')
            control_queue.put(key)
            break

    time.sleep(1)
    record_process.terminate()
    record_process.join()

