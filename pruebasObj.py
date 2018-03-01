import api.ps_drone as ps_drone
import time
#import RPi.GPIO as GPIO
import vision
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
tiempoAnt = time.time()
while not stop:
	frame = getImage()
	coordX, coordY = vision.getCenter(frame)
	cv2.imshow("Imagen",frame)
	cv2.waitKey(1)
	if(coordY==-1 or coordX==-1):
		#Didn't find and object m8
		print "No object found on frame"
		#drone.stop()
		#drone.hover()
	else:
		print "Found an object on frame"
		#stop = True
		#LLamar al PID
		
		#drone.move(SpeedX,0.1,SpeedY,0)
	#stop=(GPIO.input(INICIO)==0)	
#Exiting the program
drone.stopVideo()
drone.shutdown()
cv2.destroyAllWindows()
#GPIO.cleanup()
