import cv2
import numpy as np
import sys
import time
import vision
sys.path.insert(0, '../')
import api.ps_drone as ps_drone
def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage 
    pImg = cv2.resize(img,(640, 360), interpolation = cv2.INTER_CUBIC)               
    return pImg      # Returns image

print "Booting up the drone for color calibration"
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
while CDC == drone.ConfigDataCount: time.sleep(0.0001)  # Wait until it is done (after resync is done)
drone.startVideo()
vision.setRange()
k=0
while k != 27:
	frame =  getImage()
	area, frame = vision.getVentana(frame)
	cv2.imshow("Ventana mas grande", frame)
	k =cv2.waitKey(5)%256
cv2.destroyAllWindows()