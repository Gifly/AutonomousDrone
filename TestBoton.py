import api.ps_drone as ps_drone
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

TRIG = 3
ECHO = 2
INICIO = 4

drone = ps_drone.Drone()  # Start using drone
print "Configuracion del drone"
drone.startup()  # Connects to drone and starts subprocesses
drone.reset()  # Always good, at start
drone.trim()                                       # Recalibrate sensors
drone.getSelfRotation(5)
time.sleep(0.5)
print "Configuracion de los pines"
GPIO.setup(INICIO, GPIO.IN)
while GPIO.input(INICIO)==0:
        pass
	#Nada solo se queda aqui
print "Comienzo el programa"
print "takeoff"
drone.takeoff()
time.sleep(2)

print "hovering"
drone.hover()
time.sleep(3)

print "land"
drone.land()
