##################################################################################################
###### Playground																			######
##################################################################################################
###
### Here you can write your first test-codes and play around with them
###
import time
from api import ps_drone
import pygame
import cv2

def usarVideo():
	print "Mostrar video"
	IMC = 	 drone.VideoImageCount	
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	#key = drone.getKey()
	#if key:		stop = True
	img  = drone.VideoImage					# Copy video-image
	pImg = cv2.resize(img,(360,640))
	return img		# Process video-image
						

pygame.init()
screen = pygame.display.set_mode((320, 240))
drone = ps_drone.Drone()								# Start using drone					
drone.startup()
drone.reset()
drone.trim()                                       # Recalibrate sensors
drone.getSelfRotation(5)                           # Get auto-alteration of gyroscope-sensor
print "Drone inicializado"
drone.setConfigAllID()
print "Proceso de configuracion"
drone.sdVideo()
drone.frontCam()
drone.startVideo()
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:	time.sleep(0.0001)	# Wait until it is done (after resync is done)
drone.startVideo()					# Start video-function
print "Setting up the video options"
time.sleep(2)
camFron = True
stop = False
mostrarImg = False
print "Listo para recibir comandos"
while not stop:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			stop=True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.display.quit()
				pygame.quit()
				stop=True
			elif event.key == pygame.K_w:
				drone.moveForward()
			elif event.key == pygame.K_s:
				drone.moveBackward()
			elif event.key == pygame.K_a:
				drone.moveLeft()
			elif event.key == pygame.K_d:
				drone.moveRight()
			elif event.key == pygame.K_q:
				drone.turnLeft(	)
			elif event.key == pygame.K_e:
				drone.turnRight()
			elif event.key == pygame.K_UP:
				drone.moveUp()
			elif event.key == pygame.K_DOWN:
				drone.moveDown()
			elif event.key == pygame.K_RETURN:
				print "up"
				drone.takeoff()
			elif event.key == pygame.K_SPACE:
				drone.land()
			elif event.key == pygame.K_p:
				mostrarImgF()
			elif event.key == pygame.K_v:
				mostrarImg=True
				print "video encendido"
			elif event.key == pygame.K_t:
				if(camFron):
					drone.groundCam()
					camFron= not camFron
				else:
					drone.frontCam()
		elif event.type == pygame.KEYUP:
			drone.hover()
	if(mostrarImg):
		pImg = usarVideo()
		print "Muestro la imagen actual"
		cv2.imshow('Drones video',pImg)			# Show processed video-image
		stop = (cv2.waitKey(1) ==13)		#bat = drone.getBattery()[0]
	#print bat
	#drone.showVideo(False)
	#f = pygame.font.Font(None, 20)
	#hud = f.render('Battery: %i%%' % bat, True, (255,0,0))
	#screen.blit(hud,(10,10))
cv2.destroyAllWindows()
pygame.display.quit()
pygame.quit()
sys.exit()


