from api import ps_drone
import time
import opencv

drone = ps_drone.Drone()								# Start using drone					
drone.startup()
drone.reset()
drone.trim()                                       # Recalibrate sensors
drone.getSelfRotation(5) 
drone.setConfigAllID()
#Estos comandos se deben de correr para poder utilizar la camara
print "Proceso de configuracion de la camara"
drone.sdVideo()
drone.frontCam()
drone.startVideo()
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:	time.sleep(0.0001)	# Wait until it is done (after resync is done)
drone.startVideo()
print "Termine exitosamente la configuracion"
#Funcion que regresa un frame del video del dron
	
def getImage():
	print "Tomo una imagen (getImage)"
	IMC = drone.VideoImageCount	
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	img  = drone.VideoImage					# Copy video-image
	pImg = cv2.resize(img,(360,640))
	return img		# Returns image

def getCenter():
	frame = getImage()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Define COLORROSAQLERO range (CHECKKKKKKKKKKKKKKKKKKK)
	lower = np.array([100, 150, 200])
	upper = np.array([255, 255, 255])
	mask = cv2.inRange(hsv, lower, upper)
	res = cv2.bitwise_and(frame, frame, mask=mask)
	res = cv2.medianBlur(res, 5)
	cv2.imshow('Original image', frame)
	cv2.imshow('Color Detector', res)

	M = cv2.moments(mask)
	x=-1
	y=-1

	if(M['m00'] != 0):
		x = int(M['m10'] / M['m00'])
		y = int(M['m01'] / M['m00'])
	print x
	print y
	return x, y
