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
	IMC = drone.VideoImageCount	
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	img  = drone.VideoImage					# Copy video-image
	pImg = cv2.resize(img,(640,360), interpolation = cv2.INTER_CUBIC)
	return img		# Returns image

#INICIO = 2
#Sets the pin's configuration
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(INICIO, GPIO.IN)
#Drone initial configuration
SpeedX=0.0
SpeedY=0.0
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
PIDx = PIDrone.DronePID(0.045, 0.051, 0)
PIDy = PIDrone.DronePID(0.21, 0.12, 0)
print "Initial configuration complete"
print 'BATTERY: ',drone.getBattery()[0]
#Waits for the Inicio button to be activated
#while GPIO.input(INICIO)==0:
	#pass
print "Button pressed, starting mission, buckle up"


drone.takeoff()
time.sleep(2)
drone.hover()
print "Hovering waiting for an object to be detected"
stop = False
k=0
SpeedZ = 0.0
#tiempoAnt = time.time()
while k != 27:	
	frame = getImage()
	coordX, coordY, area = vision.getCenter(frame)
	if(area>0):
		distance = 4000000*pow(area,-0.709)
	SpeedX = -1.0*PIDx.getVelocity(0.05,320,coordX)
	SpeedY = PIDy.getVelocity(0.05,180,coordY)
	font = cv2.FONT_ITALIC
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
		cv2.circle(frame, (coordX,coordY),5,(66,244,66),-1)
		if(SpeedX==0.0 and SpeedY==0.0):
			drone.stop()
			time.sleep(0.01)
			#if(distance>40):
				#SpeedZ=0.09
			#else:
				#SpeedZ=0.0
			drone.move(SpeedX,SpeedZ,SpeedY,0.0)
		else:
			drone.move(SpeedX, SpeedZ, SpeedY, 0.0)
	print "Velocidades: ",SpeedX,SpeedY,SpeedZ
	FlechaX=SpeedX*620/0.50
	FlechaY=-SpeedY*320/0.50
	cv2.line(frame,(320,180),(int(FlechaX)+320,int(FlechaY)+180),(66,244,66),3)
	print(SpeedX, SpeedY)
	print(FlechaX,FlechaY)
	cv2.putText(frame,str(SpeedX),(50,20),font,0.5,(255,255,255),1)
	cv2.putText(frame,str(SpeedY),(50,50),font,0.5,(255,255,255),1)
	cv2.imshow("Original image",frame)	
	k =cv2.waitKey(5)%256
#Exiting the program
drone.land()
drone.stopVideo()
drone.shutdown()
cv2.destroyAllWindows()
#GPIO.cleanup()
