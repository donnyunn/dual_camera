import video

v = video.opencv()

v.initCameraDuo('/dev/video0', '/dev/video2')

while True:
    frame = v.getCameraFrame()
    v.playFrame(frame)

    key = v.waitKey(1)
    if key & 0xff == ord('q'):
        break
    