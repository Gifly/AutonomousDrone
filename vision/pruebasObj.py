import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time
#import RPi.GPIO as GPIO
from vision import vision
import cv2
from PID import PIDrone
#importar libreria de Christian aqui

def getImage():
	#print "Tomo una imagen (getImage)"
	IMC = drone.VideoImageCount	
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	img  = drone.VideoImage					# Copy video-image
	pImg = cv2.resize(img,(360,640))
	return img		# Returns image


print "Booting up the drone"
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
while CDC == drone.ConfigDataCount:	time.sleep(0.0001)	# Wait until it is done (after resync is done)
drone.startVideo()
PIDx = PIDrone.DronePID(0.051, 0.047, 0)
PIDy = PIDrone.DronePID(0.091, 0.12, 0)
print "Initial configuration complete"
SpeedX=0
SpeedY=0
areaIdeal = 360*640/3

#Waits for the Inicio button to be activated
#while GPIO.input(INICIO)==0:
	#pass
print "Button pressed, starting mission, buckle up!"

#drone.takeoff()
#time.sleep(2)
#drone.hover()
print "Hovering waiting for an object to be detected"
stop = False
tiempoAnt = time.time()
k=0

while k != 27:   
	frame = getImage()
	IndicatorDistance, frame = vision.getIndicators(frame)
	print "Distancia entre indicadores: ", IndicatorDistance
	coordX, coordY, area = vision.getCenter(frame)
	FlechaX=SpeedX*620/0.50
	FlechaY=-SpeedY*320/0.50
	cv2.line(frame,(320,180),(int(FlechaX)+320,int(FlechaY)+180),(66,244,66),3)
	SpeedX = -1.0*PIDx.getVelocity(0.05,320,coordX)
	SpeedY = PIDy.getVelocity(0.05,180,coordY)
	font = cv2.FONT_ITALIC
	#if(SpeedX<0.09 and SpeedX>0.05):
	#	SpeedX = 0.05
	#elif(SpeedX<0.05):
	#	SpeedX=0.0
	
	if(coordY==-1 or coordX==-1):
		#Didn't find and object m8
		print "No object found on frame"
		SpeedX=0.0
		SpeedY=0.0


	else:
		cv2.circle(frame, (coordX,coordY),5,(66,244,66),-1)
		
		print "Found an object on frame"
	#print(SpeedX, SpeedY)
	#print(FlechaX,FlechaY)
	cv2.putText(frame,str(SpeedX),(50,30),font,1,(255,255,255),1)
	cv2.putText(frame,str(SpeedY),(50,60),font,1,(255,255,255),1)

	cv2.imshow("Original image",frame)
	k =cv2.waitKey(5)%256
print "Exiting the program"		
drone.stopVideo()
drone.shutdown()
cv2.destroyAllWindows()
cv2.destroyAllWindows()

