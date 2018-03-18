

import cv2
import numpy as np
import sys
import time
sys.path.insert(0, '../')
from vision import vision
import api.ps_drone as ps_drone

def getFrameGround():
	IMC = drone.VideoImageCount
	while drone.VideoImageCount==IMC: time.sleep(0.01)	
	drone.groundVideo()  
	img = drone.VideoImage 
	return img

print "Booting up the drone"
drone = ps_drone.Drone()                           # Start using drone	
drone.startup()                                    # Connects to drone and starts subprocesses
drone.trim()                                     
drone.getSelfRotation(5) 
drone.reset()                                      # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
drone.useDemoMode(False)                    # Set 15 basic dataset/sec
drone.setConfigAllID()
drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
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


NDC = drone.NavDataCount
alti = 0.0
target = 1800
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

exit = False
for i in range(0,4):
	#LEFT FORWARD
	# drone.move(-0.1,0.03,0.0,0.0) #RIGTH, FORWARD, UP, TURN RIGHT
	if exit:
		break

	past = time.time()
	now = time.time()
	while (now - past) < 4:
		if (i % 2) == 0:
			drone.move(-0.08,0.03,0.0,0.0) #RIGTH, FORWARD, UP, TURN RIGHT
		else:
			drone.move(0.08,0.03,0.0,0.0) #RIGTH, FORWARD, UP, TURN RIGHT
		img = getFrameGround()
		cv2.imshow("ground",img)
		x,y,area = vision.getBase(img)
		print x,y
		if area > 0:
			cv2.imwrite("/home/alex/Pictures/" + str(area) + ".jpg",img)
		if x > -1 and y > -1:
			print "FOUND!!"
			exit = True
			break
		now = time.time()


drone.hover()
time.sleep(2)

while 1:
	img = getFrameGround()
	cv2.imshow("ground",img)
	print vision.getBase(img)
	k = cv2.waitKey(20)
	if k == 1048586:
		break

drone.land()

cv2.destroyAllWindows()