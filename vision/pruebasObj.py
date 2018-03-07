import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time
#import RPi.GPIO as GPIO
from vision import vision
import cv2
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
print "Initial configuration complete"
#Waits for the Inicio button to be activated
#while GPIO.input(INICIO)==0:
	#pass
print "Button pressed, starting mission, buckle up"

#drone.takeoff()
#time.sleep(2)
#drone.hover()
print "Hovering waiting for an object to be detected"
stop = False
distance =0
k=0
while k != 27:
	frame = getImage()
	coordX, coordY, area = vision.getCenter(frame)
	cv2.imshow("Imagen",frame)
	if(coordY==-1 or coordX==-1):
		#Didn't find and object m8
		print "No object found on frame"
		#drone.stop()
		#drone.hover()
		distance =0.0
	else:
		print "Found an object on frame"
		if(area>0):
			distance = 4000000*pow(area,-0.709)
		print distance
		#stop = True
		#LLamar al PID
	k = cv2.waitKey(5)%256
		#drone.move(SpeedX,0.1,SpeedY,0)
	#stop=(GPIO.input(INICIO)==0)	
#Exiting the program
drone.stopVideo()
drone.shutdown()
cv2.destroyAllWindows()
cv2.destroyAllWindows()
#GPIO.cleanup()
