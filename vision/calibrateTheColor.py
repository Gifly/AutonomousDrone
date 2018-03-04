import cv2
import numpy as np
# Roborregos libs
import sys
sys.path.insert(0, '../lib/')
#import Larc_vision_2017 as rb

cap = cv2.VideoCapture(0)
cv2.namedWindow('HSV',cv2.WINDOW_NORMAL)
cv2.namedWindow('BGR',cv2.WINDOW_NORMAL)
cv2.resizeWindow('BGR', 300,50)
cv2.resizeWindow('HSV', 300,50)

def nothing(x):
    pass

# create trackbars for color change
cv2.createTrackbar('HL','HSV',0,255,nothing)
cv2.createTrackbar('SL','HSV',0,255,nothing)
cv2.createTrackbar('VL','HSV',0,255,nothing)
cv2.createTrackbar('HU','HSV',0,255,nothing)
cv2.createTrackbar('SU','HSV',0,255,nothing)
cv2.createTrackbar('VU','HSV',0,255,nothing)

testColor = np.zeros((100,200,3), np.uint8)

# create trackbars for color change
cv2.createTrackbar('R','BGR',0,255,nothing)
cv2.createTrackbar('G','BGR',0,255,nothing)
cv2.createTrackbar('B','BGR',0,255,nothing)

while(1):

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame,(640, 480), interpolation = cv2.INTER_CUBIC)


    hl = cv2.getTrackbarPos('HL', 'HSV')
    sl = cv2.getTrackbarPos('SL', 'HSV')
    vl = cv2.getTrackbarPos('VL', 'HSV')
    hu = cv2.getTrackbarPos('HU', 'HSV')
    su = cv2.getTrackbarPos('SU', 'HSV')
    vu = cv2.getTrackbarPos('VU', 'HSV')

    b = cv2.getTrackbarPos('B', 'BGR')
    g = cv2.getTrackbarPos('G', 'BGR')
    r = cv2.getTrackbarPos('R', 'BGR')

    testColor[:] = [b,g,r]
    colorToTrack = np.uint8([[[b, g, r]]])
    hsv_color = cv2.cvtColor(colorToTrack, cv2.COLOR_BGR2HSV)
    print hsv_color

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    #lower = np.array([h-20,100,100])
    #upper = np.array([h+20,s,v])
    lower = np.array([hl, sl, vl])
    upper = np.array([hu, su, vu])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow('frame',frame)
    # cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('original', frame)
    cv2.imshow('color',testColor)

    #rb.getTankCenter(frame)
    #break
    k = cv2.waitKey(5)
    if k == 27:
        break

cv2.destroyAllWindows()
file = open("colorVal.txt", "w")
file.write(str(hl) + "\n")
file.write(str(sl) + "\n")
file.write(str(vl) + "\n")
file.write(str(hu) + "\n")
file.write(str(su) + "\n")
file.write(str(vu) + "\n")
file.close()
