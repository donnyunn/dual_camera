import video
import defines

mode = defines.MODE()
v = video.opencv()

FPS = v.initCameraDuo('/dev/video0', '/dev/video2')
print(FPS)

frame_rec = []
rec_cnt = 0
play_cnt = 0
delay_cnt = 0
slow_cnt = 0

state = mode.STOP
delay_sec = 0

frame = v.getCameraFrame()
v.playFrame(frame)

while True:
    if state == mode.PLAY:
        # get frame
        frame = v.getCameraFrame()

        # debug
        curr_time = play_cnt / FPS + delay_sec
        rec_time = rec_cnt / FPS + delay_sec
        dbgmsg = f'delay {delay_sec} sec, ' + f'current {curr_time:.1f} sec, ' + f'recording {rec_time:.1f} sec'
        # dbgmsg = f'delay_sec({delay_sec}), rec_cnt({rec_cnt}), play_cnt({play_cnt})'
        frame = v.getFrameTexted(frame, dbgmsg)

        # record
        frame_rec.append(frame)
        rec_cnt = rec_cnt + 1

        # play with delayed
        if rec_cnt > delay_cnt:
            frame_play = frame_rec[play_cnt]
            play_cnt = play_cnt + 1
        else:
            frame_play = frame_rec[play_cnt]
        
        v.playFrame(frame_play)

        if (rec_cnt > (FPS * 12)):
            state = mode.STOP
    
    elif state == mode.SLOW_PLAY:
        if slow_cnt % FPS == 0:
            play_cnt = play_cnt + 1

            if play_cnt >= rec_cnt:
                play_cnt = 0
            frame_play = frame_rec[play_cnt]
            v.playFrame(frame_play)
        
        slow_cnt = slow_cnt + 1

    key = v.waitKey(1)    
    if key & 0xff == ord('s'):
        if state == mode.PLAY:
            play_cnt = 0
            state = mode.SLOW_PLAY
        elif state == mode.SLOW_PLAY:
            delay_cnt = int(delay_sec * FPS)
            frame_rec.clear()
            frame_cnt = 0
            play_cnt = 0
            rec_cnt = 0
            state = mode.PLAY
    elif key & 0xff == ord('p'):
        if state == mode.PLAY:
            state = mode.STOP
        elif state == mode.STOP:
            state = mode.PLAY
        elif state == mode.SLOW_PLAY:
            state = mode.SLOW_STOP
        elif state == mode.SLOW_STOP:
            state = mode.SLOW_PLAY
    elif key & 0xff == ord('a'):
        if play_cnt > 15:
            play_cnt = play_cnt - 15
            if state == mode.STOP or state == mode.SLOW_STOP:
                v.playFrame(frame_rec[play_cnt])
    elif key & 0xff == ord('d'):
        if play_cnt < (rec_cnt - 15):
            play_cnt = play_cnt + 15
            if state == mode.STOP or state == mode.SLOW_STOP:
                v.playFrame(frame_rec[play_cnt])
    elif key & 0xff == ord('0'):
        delay_sec = 0
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('1'):
        delay_sec = 1
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('2'):
        delay_sec = 2
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('3'):
        delay_sec = 3
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('4'):
        delay_sec = 4
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('5'):
        delay_sec = 5
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('6'):
        delay_sec = 6
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('7'):
        delay_sec = 7
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('8'):
        delay_sec = 8
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('9'):
        delay_sec = 9
        delay_cnt = int(delay_sec * FPS)
        frame_rec.clear()
        frame_cnt = 0
        play_cnt = 0
        rec_cnt = 0
        state = mode.PLAY
    elif key & 0xff == ord('q'):
        break

v.quit()