import time
import cv2 
import numpy as np
import math
import os
lowVal=[]
uppVal=[]
lowValInd=[]
uppValInd=[]
def setRange():
	cwd = os.getcwd()
	print "cwd: ",cwd
	file = open("../vision/colorV.txt","r")
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
def getCenter(frame):
	
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Define COLORROSAQLERO range (CHECKKKKKKKKKKKKKKKKKKK)
	lower = np.array(lowVal)
	upper = np.array(uppVal)
	mask = cv2.inRange(hsv, lower, upper)
	#cv2.imshow('mask',mask)
	res = cv2.bitwise_and(frame, frame, mask=mask)
	res = cv2.medianBlur(res, 5)
	cv2.imshow('Original image', frame)
	M = cv2.moments(mask)
	area = M['m00']
	x=-1
	y=-1 
	if(area >100000):
		x = int(M['m10'] / M['m00'])
		y = int(M['m01'] / M['m00'])
		cv2.circle(res, (x,y),5,(66,244,66),-1)
	cv2.imshow('Color Detector', res)
	print x, y, area
	return x, y,area

def getIndicators(frame):  
	
	Puntos =[]
	
	kernel = np.ones((5,5),np.uint8)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lowerInd = np.array ([lowValInd[0],lowValInd[1],lowValInd[2]])
	upperInd = np.array([uppValInd[0],uppValInd[1],uppValInd[2]])
	maskInd = cv2.inRange(hsv,lowerInd,upperInd)
	maskInd = cv2.morphologyEx(maskInd,cv2.MORPH_OPEN,kernel)
	contours , hierarchy = cv2.findContours(maskInd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	n = len(contours)
	contours = sorted(contours,key=cv2.contourArea, reverse=True)[:n]
	if(len(contours)>=2):
		for i in range (0,2):
			if(isCircle(contours[i])):
				Puntos.append(contours[i])
    
	distance = -1
	#Gets X and Y axis of both points
	if(Puntos):
		cv2.drawContours(frame,Puntos,-1,(0,255,0),2)
	if(len(Puntos)>=2):
		P1 = cv2.moments(Puntos[0])
		P2 = cv2.moments(Puntos[1])
		Px1 = int(P1['m10'] / P1['m00'])
		Py1 = int(P1['m01'] / P1['m00'])

		Px2 = int(P2['m10'] / P2['m00'])
		Py2 = int(P2['m01'] / P2['m00'])
	#Calculates relative distance between points
		distance = math.sqrt(pow(Px1-Px2,2)+pow(Px1-Px2,2))
	#cv2.imshow('Indicators',frame)
	return distance, len(Puntos), frame

		

    #Encontrar los centros or wtvr

def isCircle(cnt):
	template = cv2.imread('../vision/images/circle.jpg',0)
	ret, thresh = cv2.threshold(template, 127, 255, 0)

	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

	match = cv2.matchShapes(contours[0], cnt, 1, 0.0)

	if match < 0.45:
		return True
	return False

def getPared(frame,lowT):
	Rectan=[]
	area=0
	kernel = np.ones((5,5),np.uint8)
	#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frameCl = cv2.morphologyEx(frame,cv2.MORPH_OPEN,kernel)
	frameCl = cv2.bilateralFilter(frameCl,9,75,75)
	kanye = cv2.Canny(frameCl,lowT, 3*lowT)
	cv2.imshow("Canny",kanye)
	contours , hierarchy = cv2.findContours(kanye, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	n = len(contours)
	#print n
	contours = sorted(contours,key=cv2.contourArea, reverse=True)[:n]
	cv2.drawContours(frame,contours,-1,(0,50,0),1)
	if(len(contours)>=1):
		cv2.drawContours(frame,contours[0],-1,(255,0,0),2)
		if(isRectangle(contours[0])):
			#print "Encontre un rectangulo"
			cv2.drawContours(frame,contours[0],-1,(0,0,255),2)
    		M = cv2.moments(contours[0])
    		area = M['m00']
	return area,frame
	#Gets X and Y axis of both points

def isRectangle(cnt):
	template = cv2.imread('../vision/images/rectangle.png',0)
	ret, thresh = cv2.threshold(template, 127, 255, 0)

	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

	match = cv2.matchShapes(contours[0], cnt, 1, 0.0)

	if match < 0.20:
		return True
	return False
