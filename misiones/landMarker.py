

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
drone.useDemoMode(True)                    # Set 15 basic dataset/sec
drone.setConfigAllID()
drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])

print "Booting up the camera"
drone.sdVideo()                                     # Choose lower resolution (try hdVideo())
drone.frontCam()                                    # Choose front view
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
while alti < 1600:
	while drone.NavDataCount == NDC:   time.sleep(0.001)
	NDC = drone.NavDataCount
	alti = drone.NavData["altitude"][3]
	print "Altitude: " + str(alti)
	drone.moveUp(0.9)

for i in range(0,2):
	drone.moveForward()
	drone.moveLeft()

	time.sleep(2)

	drone.moveForward()
	drone.moveRight()

	time.sleep(2)



cv2.destroyAllWindows()