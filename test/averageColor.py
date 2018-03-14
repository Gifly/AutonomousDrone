import time
import cv2 
import numpy as np
import sys
sys.path.insert(0, '../')
import api.ps_drone as ps_drone
from vision import vision

def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage 
    pImg = cv2.resize(img,(640, 360), interpolation = cv2.INTER_CUBIC)               
    return pImg      # Returns image


def avrgColor(frame):
	frame2 = frame.copy()
	frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
	H, S, V = cv2.split(frame2)
	Havg = np.mean(H)
	Savg = np.mean(S)
	Vavg = np.mean(V)
	totalMean = np.mean([Havg,Savg,Vavg])
	font = cv2.FONT_ITALIC
	cv2.putText(frame,str(Havg),(50,50),font,0.5,(255,201,255),2)
	cv2.putText(frame,str(Savg),(50,70),font,0.5,(255,201,255),2)
	cv2.putText(frame,str(Vavg),(50,90),font,0.5,(255,201,255),2)
	cv2.putText(frame,str(totalMean),(50,120),font,0.5,(255,201,255),2)
	return Havg , Savg, Vavg, frame


print "Booting up the drone for color Average"
drone = ps_drone.Drone()                                                    
drone.startup()
drone.reset()
drone.trim()                                     
drone.getSelfRotation(5) 
drone.setConfigAllID()
#Drone's camera initial configuration
print "Booting up the camera"
drone.frontCam()
drone.hdVideo()
drone.startVideo()
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount: time.sleep(0.0001)  # Wait until it is done (after resync is done)
drone.startVideo()



k = 0
lowT=50
print "h - j "
while k!=27:
	frame = getImage()
	area, frame = vision.getPared(frame, lowT)
	cv2.imshow("Average colors", frame)
	k =cv2.waitKey(5)%256
	if(k==74):
		lowT+=10
		print"mas", lowT
	elif(k==72):
		lowT-=10
		print "menos", lowT
cv2.destroyAllWindows()