import cv2
import numpy as np
import sys
import time
sys.path.insert(0, '../')
from PID import PIDrone
from vision import vision
import api.ps_drone as ps_drone
from tools import emergency

def getFrameGround():
	IMC = drone.VideoImageCount
	while drone.VideoImageCount==IMC: time.sleep(0.01)	
	drone.groundVideo()  
	img = drone.VideoImage 
	return img

print "Booting up the drone"
drone = ps_drone.Drone()                           # Start using drone	
thread = emergency.keyThread(drone)
drone.startup()                                    # Connects to drone and starts subprocesses
drone.trim()                                     
drone.getSelfRotation(5) 
drone.reset()                                      # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
drone.useDemoMode(False)                    # Set 15 basic dataset/sec
drone.setConfigAllID()
drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
thread.start()
print "BATERIA ACTUAL: ", drone.getBattery()[0]

print "Booting up the camera"
drone.sdVideo()                                     # Choose lower resolution (try hdVideo())
drone.groundCam()                                    # Choose front view
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: time.sleep(0.001) # Wait until it is done (after resync)
drone.startVideo()                                  # Start video-function

#NAVIGATE THE ARENA
drone.showVideo()

drone.takeoff()
time.sleep(2)
drone.hover()
time.sleep(2)

#THE DRONE GET A DECENT ALTITUDE TO DETECT THE MARKER
NDC = drone.NavDataCount
alti = 0.0
target = 2000
while alti < target:
	while drone.NavDataCount == NDC:   time.sleep(0.001)
	NDC = drone.NavDataCount
	alti = drone.NavData["altitude"][3]
	print "Altitude: " + str(alti)
	if alti >= target:
		break 
	drone.moveUp(0.9)

drone.moveDown(0.5)
time.sleep(0.5)

#THE DRONE LOOKS FOR THE MARKER DOING ZIGZAG 
exit = False
x = y = -1
area = 0
for i in range(0,4):
	if exit:
		break

	past = time.time()
	now = time.time()
	while (now - past) < 4:
		if (i % 2) == 0:
			drone.move(-0.07,0.02,0.0,0.0) #RIGTH, FORWARD, UP, TURN RIGHT
		else:
			drone.move(0.07,0.02,0.0,0.0) #RIGTH, FORWARD, UP, TURN RIGHT
		img = getFrameGround()
		cv2.imshow("ground",img)
		x,y,area = vision.getBase(img)
		print x,y
		if area > 0:
			cv2.imwrite("/home/paul/Pictures/" + str(area) + ".jpg",img)
		if x > -1 and y > -1 and area > 25000:
			print "FOUND!!"
			exit = True
			break
		now = time.time()

drone.hover()
time.sleep(2)

#INITIALIZE PID HERE
print "Inicializo el PID"
PIDx = PIDrone.DronePID(0.090, 0.02, 0)
PIDy = PIDrone.DronePID(0.081, 0.02, 0)
SpeedX = 0.0
SpeedY = 0.0

#THIS PART OF THE CODE ALLIGNS TO THE MARKER ONCE FOUND
cenX = 320
cenY = 180
tolerance = 100
xL=0.0
yL=0.0
while abs(SpeedX) !=0.063 and abs(SpeedY)!=0.063  :
	print "Me alineo"
	drone.hover()
	cenX = 320
	cenY = 180
	tolerance = 100
	img = getFrameGround()
	cv2.imshow("ground",img)
	k = cv2.waitKey(20)
	xL,yL,areaL = vision.getBase(img)
	print xL,yL,areaL
	SpeedX = PIDx.getVelocity(0.005,320,xL)
	SpeedY = PIDy.getVelocity(0.005,180,yL)
	print "Velocidad en X: ", SpeedX, "Velocidad en Y: ", SpeedY
	drone.move(SpeedX,SpeedY,0.0,0.0)

drone.land()
drone.shutdown()
cv2.destroyAllWindows()