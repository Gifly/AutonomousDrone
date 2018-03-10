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
		elif(i<6):
			uppVal.append(int(line))
		i+=1
	file.close()
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
	if(area >300000):
		x = int(M['m10'] / M['m00'])
		y = int(M['m01'] / M['m00'])
		cv2.circle(res, (x,y),5,(66,244,66),-1)
	cv2.imshow('Color Detector', res)
	print x, y, area
	return x, y,area

def getIndicators(frame):  
	file = open('colorVal.txt')
	lowValInd=[]
	uppValInd=[]
	Puntos =[]
	i=0
	for line in file:
		if(i>6):
			lowValInd.append(int(line))
		elif(i>9):
			#print line
			uppValInd.append(int(line))
		i+=1
	file.close()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lowerInd = np.array ([lowValInd[0],lowValInd[1],lowValInd[2]])
	upperInd = np.array([uppValInd[0],uppValInd[1],uppValInd[2]])
	maskInd = cv2.inRange(hsv,lowerInd,upperInd)
	maskInd = cv2.morphologyEx(maskInd,cv2.MORPH_OPEN,kernel)
	contours , hierarchy = cv2.findContours(maskInd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	n = len(contours)
	contours = sorted(contours,key=cv2.contourArea, reverse=True)[:n]
	print len(contours)
    if(len(contours)>=2):
        for i in range (0,2):
            if(isCircle(contours[i])):
                Puntos.append(contours[i])
    
    distance = -1
    #Gets X and Y axis of both points
    if(Puntos):
        cv2.drawContours(res,Puntos,-1,(0,255,0),2)
        if(len(Puntos)>=2):
		    P1 = cv2.moments(Puntos[0])
		    P2 = cv2.moments(Puntos[1])
		    Px1 = int(P1['m10'] / P1['m00'])
			Py1 = int(P1['m01'] / P1['m00'])
			
			Px2 = int(P2['m10'] / P2['m00'])
			Py2 = int(P2['m01'] / P2['m00'])
		#Calculates relative distance between points 
			distance = sqrt(pow(Px1-PX2,2)+pow(Px1-PX2,2))
	cv2.imshow('Indicators',res)
	return distance, res

		

    #Encontrar los centros or wtvr

def isCircle(cnt):
	template = cv2.imread('images/circle.jpg',0)
	ret, thresh = cv2.threshold(template, 127, 255, 0)

	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

	match = cv2.matchShapes(contours[0], cnt, 1, 0.0)

	if match < 0.45:
		return True
	return False