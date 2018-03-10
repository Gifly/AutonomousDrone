import time
import cv2 
import numpy as np
def getCenter(frame):
	file = open("colorVal.txt","r")
	lowVal=[]
	uppVal=[]
	lowValInd=[]
	uppValInd=[]
	i=0
	for line in file:
		if(i<3):
			lowVal.append(int(line))
		elif(i<6):
			uppVal.append(int(line))
		elif(i<9):
			lowValInd.append(int(line))
		else:
			uppValInd.append(int(line))
		i+=1
	file.close()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Define COLORROSAQLERO range (CHECKKKKKKKKKKKKKKKKKKK)
	lower = np.array(lowVal)
	upper = np.array(uppVal)
	lowerInd = np.array (lowValInd)
	upperInd = np.array(uppValInd)
	mask = cv2.inRange(hsv, lower, upper)
	maskInd = cv2.inRange(hsv,lowerInd,upperInd)
	cv2.imshow('Puntitos',cv2.bitwise_and(hsv,hsv,mask=maskInd))
	contours , hierarchy = cv2.findContours(maskInd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(frame,contours,-1,(0,255,0),-1)
	#cv2.imshow('mask',mask)
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
