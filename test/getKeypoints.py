import cv2
import numpy as np
import sys
import vision
sys.path.insert(0, '../')
import api.ps_drone as ps_drone

cap = cv2.VideoCapture(1)
fast = cv2.FastFeatureDetector()

def getImage():
	IMC = drone.VideoImageCount	
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	img  = drone.VideoImage					# Copy video-image
	pImg = cv2.resize(img,(640,360), interpolation = cv2.INTER_CUBIC)
	return img		# Returns image

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

while True:

    # Get webcam images
    image = getImage()

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Obtain Key points, by default non max suppression is On
	# to turn off set fast.setBool('nonmaxSuppression', False)
	keypoints = fast.detect(gray, None)
	print "Number of keypoints Detected: ", len(keypoints)

	# Draw rich keypoints on input image
	image = cv2.drawKeypoints(image, keypoints, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	cv2.imshow('keypnts', image)
	cv2.waitKey()
cv2.waitKey()
cv2.destroyAllWindows()
