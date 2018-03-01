import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time
#import RPi.GPIO as GPIO
import vision
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
PIDr = PIDrone.DronePID(0.05, 0.01, 0)
print "Initial configuration complete"
#Waits for the Inicio button to be activated
#while GPIO.input(INICIO)==0:
	#pass
print "Button pressed, starting mission, buckle up"


drone.takeoff()
time.sleep(2)
drone.hover()

print "Hovering waiting for an object to be detected"
stop = False
tiempoAnt = time.time()
while not stop:
	frame = getImage()
	coordX, coordY = vision.getCenter(frame)
	cv2.waitKey(1)
	SpeedX = -1.0*PIDr.getVelocity(0.05,320,coordX)
	print SpeedX
	if(coordY==-1 or coordX==-1 or SpeedX==0):
		#Didn't find and object m8
		print "No object found on frame"
		drone.stop()
	else:
		print "Found an object on frame"
		drone.move(SpeedX, 0.0, 0.0, 0.0)
	#stop=(GPIO.input(INICIO)==0)	
#Exiting the program
drone.land()
drone.stopVideo()
drone.shutdown()
cv2.destroyAllWindows()
#GPIO.cleanup()
