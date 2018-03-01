import RPi.GPIO as GPIO
import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time

GPIO.setmode(GPIO.BCM)

TRIG = 15
ECHO = 18
INICIO = 2

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def getDistance():
  valores = []
  total =0.0
  for i in range (0,5):
    valores.append(rawDistance())
  valores.sort()
  
  total= valores[1] + valores[2] + valores[3]
  valorFil  = total/3
  return  valorFil

def rawDistance():
  GPIO.output(TRIG, False)

  time.sleep(0.005)

  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
      pass
  
  pulse_start = time.time()

  while GPIO.input(ECHO)==1:
      pass
  
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
    #drone.getSelfRotation(5)
    time.sleep(0.5)
    print drone.getBattery()[0]
    print "Configuracion de los pines"
    GPIO.setup(INICIO, GPIO.IN)
    while GPIO.input(INICIO)==0:
            pass
            print "aqui"
            #Nada solo se queda aqui
    print "Comienzo el programa"
    print "takeoff"
    drone.takeoff()
    time.sleep(2)
    drone.hover()
    time.sleep(2)
    #drone.setSpeed(0.1)
    print "hovering"
    distance = getDistance()
    while distance > 60:
        print "Distance: "
        distance = getDistance()
        print distance
        if distance <  61:
            drone.moveBackward(0.4)
        else:
            drone.moveForward(0.1)
        print "next"
        
    #time.sleep(3)
    print "back"
    drone.moveBackward(0.4)
    time.sleep(0.5)
    print "land"
    drone.land()

if __name__ == "__main__":
    main()
    GPIO.cleanup()

