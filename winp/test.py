import cv2
import numpy as np
import os

# Playing video from file:
cap = cv2.VideoCapture('example.mp4')

time_length = 42.0
fps=15
frame_seq = 625
frame_no = (frame_seq /(time_length*fps))

#cap.set(cv2.CAP_PROP_POS_FRAMES,frame_no)
print(frame_no)
#영상의 fps 가져오는것
print(cap.get(cv2.CAP_PROP_FPS))
#영상 총 프레임수
video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
print ("Number of frames: ", video_length)

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print ('Error: Creating directory of data')

currentFrame = 0
while(True):
    # Capture frame-by-frame
    cap.set(cv2.CAP_PROP_POS_FRAMES,currentFrame)
    ret, frame = cap.read()
    # Saves image of the current frame in jpg file
    name = './data/frame' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name, frame)

    # To stop duplicate images
    currentFrame += 5
    if(currentFrame > video_length):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
