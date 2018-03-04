import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time
#import RPi.GPIO as GPIO
import math
from vision import vision
import cv2
from PID import PIDrone
#importar libreria de Christian aqui

def getImage():
	print "Tomo una imagen (getImage)"
	IMC = drone.VideoImageCount	
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	img  = drone.VideoImage					# Copy video-image
	pImg = cv2.resize(img,(360,640))
	return img		# Returns image

#INICIO = 2
#Sets the pin's configuration
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(INICIO, GPIO.IN)
#Drone initial configuration
SpeedX=0.0
SpeedY=0.0
SpeedZ=0.0
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
PIDx = PIDrone.DronePID(0.47, 0.57, 0)
PIDy = PIDrone.DronePID(0.21, 0.12, 0)
PIDz = PIDrone.DronePID(0.09, 0.85, 0)
print "Initial configuration complete"
print 'BATERRY: ',drone.getBattery()[0]
#Waits for the Inicio button to be activated
#while GPIO.input(INICIO)==0:
	#pass
print "Button pressed, starting mission, buckle up"


drone.takeoff()
time.sleep(2)
drone.hover()
time.sleep(2)
print "Hovering waiting for an object to be detected"
stop = False
#tiempoAnt = time.time()
while not stop:
	print "Velocidades: ",SpeedX,SpeedY,SpeedZ
	frame = getImage()
	coordX, coordY, area = vision.getCenter(frame)
	coordZ = -37.25*(math.log(area)) + 662.85
	cv2.waitKey(1)
	SpeedX = -1.0*PIDx.getVelocity(0.05,320,coordX)
	SpeedY = PIDy.getVelocity(0.05,180,coordY)
	SpeedZ = PIDz.getVelocity(0.05,80,coordZ)
	if(coordY==-1 or coordX==-1):
		#Didn't find and object m8
		print "No object found on frame"
		SpeedX=0.0
		SpeedY=0.0
		SpeedZ=0.0
		drone.hover()
		drone.stop()
	else:
		print "Found an object on frame"
		if (SpeedX == 0.0 and SpeedY==0.0 and SpeedZ == 0.0):
			drone.stop()
		else: 
			if(coordX > 60 and coordX < 280 and coordY > 107 and coordY < 533):
				drone.move(SpeedX, SpeedZ, SpeedY, 0.0)
			else:
				drone.move(SpeedX, 0.0, SpeedY, 0.0)
	#stop=(GPIO.input(INICIO)==0)	
#Exiting the program
drone.land()
drone.stopVideo()
drone.shutdown()
cv2.destroyAllWindows()
#GPIO.cleanup()
