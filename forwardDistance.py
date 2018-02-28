import api.ps_drone as ps_drone
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

TRIG = 15
ECHO = 18
INICIO = 4

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def getDistance():
  GPIO.output(TRIG, False)

  time.sleep(0.2)

  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150

  distance = round(distance, 2)

  return distance


def main():


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
    time.sleep(5)

    print "hovering"
    #drone.hover()

    print "forward"
    distance = getDistance()
    while distance > 40:
        drone.moveForward()
        distance = getDistance()
        print distance

    print "hovering"
    drone.hover()
    time.sleep(3)

    print "land"
    drone.land()

if __name__ == "__main__":
    main()
    GPIO.cleanup()
