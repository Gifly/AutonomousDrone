import cv2
import numpy as np
import sys
sys.path.insert(0, '../lib/')

cap = cv2.VideoCapture(0)
cv2.namedWindow('HSV', cv2.WINDOW_NORMAL)
cv2.resizeWindow('HSV', 290, 250)


def nothing(x):
    pass


# create trackbars for color change
cv2.createTrackbar('HL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('SL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('VL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('HU', 'HSV', 255, 255, nothing)
cv2.createTrackbar('SU', 'HSV', 255, 255, nothing)
cv2.createTrackbar('VU', 'HSV', 255, 255, nothing)

k = 0
while k != 27:

    # Take each frame
    _, frame = cap.read()
    frame = cv2.resize(frame,(640, 480), interpolation = cv2.INTER_CUBIC)


    hl = cv2.getTrackbarPos('HL', 'HSV')
    sl = cv2.getTrackbarPos('SL', 'HSV')
    vl = cv2.getTrackbarPos('VL', 'HSV')
    hu = cv2.getTrackbarPos('HU', 'HSV')
    su = cv2.getTrackbarPos('SU', 'HSV')
    vu = cv2.getTrackbarPos('VU', 'HSV')

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range
    lower = np.array([hl, sl, vl])
    upper = np.array([hu, su, vu])

    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('res',res)
    cv2.imshow('original', frame)

    k = cv2.waitKey(5)

cv2.destroyAllWindows()
file = open("colorVal.txt", "w")
file.write(str(hl) + "\n")
file.write(str(sl) + "\n")
file.write(str(vl) + "\n")
file.write(str(hu) + "\n")
file.write(str(su) + "\n")
file.write(str(vu) + "\n")
file.close()
