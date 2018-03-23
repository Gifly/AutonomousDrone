import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time
#import RPi.GPIO as GPIO
from vision import vision
import cv2
from PID import PIDrone
from tools import emergency
#importar libreria de Christian aqui

def getImage():
	IMC = drone.VideoImageCount	
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	img  = drone.VideoImage					# Copy video-image
	pImg = cv2.resize(img,(640,360), interpolation = cv2.INTER_CUBIC)
	return img		# Returns image

k=0
SpeedZ = 0.0
SpeedX=0.0
SpeedY=0.0
print "Booting up the drone"
drone = ps_drone.Drone()
thread = emergency.keyThread(drone)													
drone.startup()
drone.reset()
drone.trim()                                     
drone.getSelfRotation(5) 
time.sleep(0.5)
thread.start()

#Drone's camera initial configuration
print "Booting up the camera"
drone.frontCam()
drone.hdVideo()
drone.startVideo()
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:	time.sleep(0.0001)	# Wait until it is done (after resync is done)
drone.startVideo()
PIDx = PIDrone.DronePID(0.050, 0.02, 0)
PIDy = PIDrone.DronePID(0.061, 0.02, 0)
print "Initial configuration complete"
print 'BATTERY: ',drone.getBattery()[0]

drone.takeoff()
time.sleep(2)
drone.hover()
time.sleep(1)
print "Hovering waiting for an object to be detected"
vision.setRange()
while k != 27:	
	frame = getImage()
	coordX, coordY, area = vision.getCenter(frame)
	distance , circulos, frame = vision.getIndicators(frame)
	SpeedX = -1.0*PIDx.getVelocity(0.005,320,coordX)
	SpeedY = PIDy.getVelocity(0.005,180,coordY)
	font = cv2.FONT_ITALIC
	print "Area: ", area
	#if(SpeedX<0.09 and SpeedX>0.05):
		#SpeedX = 0.05
	#elif(SpeedX<0.05):
		#SpeedX=0.0
	if(coordY==-1 or coordX==-1):
		#Didn't find an object m8
		print "No object found on frame"
		SpeedX=0.0
		SpeedY=0.0
		SpeedZ=0.0
		drone.hover()
		drone.stop()
		cv2.putText(frame,"Hovering",(50,70),font,0.5,(0,0,255),1)
	else:
		#Found the object on frame
		if(area>1160000):
			#If it  is too close
			SpeedZ=0.0
			cv2.putText(frame,"Muy cerca",(100,100),font,2,(255,255,255),1)
			if(SpeedX>0.05):
				SpeedX=0.04
			elif(SpeedX<-0.05):
				SpeedX=-0.04
			if(SpeedY>0.05):
				SpeedY=0.04
			elif(SpeedY<-0.05):
				SpeedY=-0.04
		else:
			#It is big enough
			SpeedZ=0.046
			
			cv2.putText(frame,"Acercandome",(100,100),font,2,(255,255,255),1)

		if(SpeedX==0.0 and SpeedY==0.0):
			if(area>1100000):
				drone.stop()
			drone.move(SpeedX,SpeedZ,SpeedY,0.0)
		else:			
			drone.move(SpeedX, SpeedZ, SpeedY, 0.0)
	cv2.circle(frame, (coordX,coordY),5,(66,244,66),-1)
	FlechaX=SpeedX*620/0.50
	FlechaY=-SpeedY*320/0.50
	cv2.line(frame,(320,180),(int(FlechaX)+320,int(FlechaY)+180),(66,244,66),3)
	#print(SpeedX, SpeedY)
	#print(FlechaX,FlechaY)
	cv2.putText(frame,str(SpeedX),(50,20),font,0.5,(255,255,255),1)
	cv2.putText(frame,str(SpeedY),(50,50),font,0.5,(255,255,255),1)
#	cv2.putText(frame,str(distance),(50,70),font,0.5,(255,255,255),1)
	cv2.imshow("Original image",frame)	
	k =cv2.waitKey(5)%256
#Exiting the program
drone.land()
drone.stopVideo()
drone.shutdown()
cv2.destroyAllWindows()
