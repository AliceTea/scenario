import cv2

#video = open('/home/jason/Videos/sheild/S04E17.mp4','r')

video = cv2.VideoCapture('/home/jason/Videos/sheild/S04E17.mp4')
limit = 60
start_time = 2000
if not video.isOpened():
    print 'file path error'
else:
    rate = video.get(cv2.cv.CV_CAP_PROP_FPS)
    size = (int(video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

    delay = 1000/rate
    success, frame = video.read()
    videoWriter = cv2.VideoWriter('/home/jason/Videos/sheild/S04E17_005.avi', cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), rate, size)
    ticks = 0
    while success:
#        cv2.imshow("Video", frame)
#        cv2.waitKey(1000 / int(rate))
        success, frame = video.read()
        if ticks >= start_time:
            videoWriter.write(frame)
        ticks = 1/rate + ticks
        if ticks >= start_time + limit:
            break
print 'over'
