import time
import cv2 
import numpy as np
def getCenter(frame):
	file = open("colorVal.txt","r")
	lowVal=[]
	uppVal=[]
	i=0
	for line in file:
		if(i<3):
			lowVal.append(int(line))
		else:
			uppVal.append(int(line))
		i+=1
	file.close()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Define COLORROSAQLERO range (CHECKKKKKKKKKKKKKKKKKKK)
	lower = np.array(lowVal)
	upper = np.array(uppVal)
	mask = cv2.inRange(hsv, lower, upper)
	res = cv2.bitwise_and(frame, frame, mask=mask)
	res = cv2.medianBlur(res, 5)
	cv2.imshow('Original image', frame)
	cv2.imshow('Color Detector', res)

	M = cv2.moments(mask)
	area = M['m00']

	x=-1
	y=-1 
	if(area >1000000):
		x = int(M['m10'] / M['m00'])
		y = int(M['m01'] / M['m00'])
	print x, y, area
	return x, y