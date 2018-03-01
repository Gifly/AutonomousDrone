import time
import cv2 
import numpy as np
def getCenter(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Define COLORROSAQLERO range (CHECKKKKKKKKKKKKKKKKKKK)
	lower = np.array([100, 150, 150])
	upper = np.array([255, 255, 255])
	mask = cv2.inRange(hsv, lower, upper)
	res = cv2.bitwise_and(frame, frame, mask=mask)
	res = cv2.medianBlur(res, 5)
	cv2.imshow('Original image', frame)
	cv2.imshow('Color Detector', res)

	M = cv2.moments(mask)
	area = M['m00']

	x=-1
	y=-1 
	if(area >500000):
		x = int(M['m10'] / M['m00'])
		y = int(M['m01'] / M['m00'])
	print x, y, area
	return x, y
