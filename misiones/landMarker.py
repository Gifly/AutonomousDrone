

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

#THE DRONE GET A DECENT ALTITUDE TO DETECT THE MARKER
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
			cv2.imwrite("/home/alex/Pictures/" + str(area) + ".jpg",img)
		if x > -1 and y > -1 and area > 25000:
			print "FOUND!!"
			exit = True
			break
		now = time.time()

drone.hover()
time.sleep(2)

#THIS PART OF THE CODE ALLIGNS TO THE MARKER ONCE FOUND

while 1:
	drone.hover()
	cenX = 320
	cenY = 180
	tolerance = 100

	img = getFrameGround()
	cv2.imshow("ground",img)
	k = cv2.waitKey(20)
	xL,yL,areaL = vision.getBase(img)
	print xL,yL,areaL

	if xL < 0 and yL < 0: #If it detects nothing moves to the last place it was detected
		if x < cenX:
			drone.moveLeft(0.1)
			time.sleep(0.5)
		elif x >= cenX:
			drone.moveRight(0.1)
			time.sleep(0.5)

		if y < cenY:
			drone.moveForward(0.1)
			time.sleep(0.5)
		elif y >= cenY:
			drone.moveBack(0.1)
			time.sleep(0.5)
		drone.moveDown(0.2)
		time.sleep(0.5)
	#ALIGN X
	if xL < (cenX - tolerance): #If its left move left
		print "ALLIGN LEFT"
		x = xL
		drone.moveLeft(0.05)
		time.sleep(0.5)
	elif xL > (cenX + tolerance): #If its right move rigth
		print "ALLIGN LEFT"
		x = xL
		drone.moveRight(0.05)
		time.sleep(0.5)

	#ALIGN Y
	if yL < (cenY - tolerance): #If its in front move forward
		print "ALLIGN FORWARD"
		y = yL
		drone.moveForward(0.05)
		time.sleep(0.5)
	elif yL > (cenY + tolerance): #If its back move back
		print "ALLIGN BACK"
		y = yL
		drone.moveBack(0.05)
		time.sleep(0.5)

	else: #It is centered
		k = 1048586

	if k == 1048586:
		break

drone.land()

cv2.destroyAllWindows()