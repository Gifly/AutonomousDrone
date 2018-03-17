import VL53L0X
import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time

def main():

    drone = ps_drone.Drone()  # Start using drone
    tof = VL53L0X.VL53L0X()
    print "Configuracion del drone"
    drone.startup()  # Connects to drone and starts subprocesses
    drone.reset()  # Always good, at start
    drone.trim()                                       # Recalibrate sensors
    #drone.getSelfRotation(5)
    time.sleep(0.5)
    print "BATERIA ACTUAL: ", drone.getBattery()[0]

    print "Comienzo el programa"
    print "takeoff"
    drone.takeoff()
    time.sleep(2)
    drone.hover()
    time.sleep(2)
    #drone.setSpeed(0.1)
    print "hovering"
    tof.start_ranging(4)
    time.sleep(0.001)
    #THIS PART GETS NEAR THE OBSTACLE
    distance = tof.get_distance()
    while distance > 1000:
        print "Distance: "
        distance = tof.get_distance()
        print distance
        if distance < 1001:
            drone.moveBackward(0.5)
        else:
            drone.moveForward(0.1)
        print "next"
    #time.sleep(3)
    print "back"
    drone.moveBackward(0.5)
    time.sleep(0.5)
    drone.hover()
    time.sleep(4)

    #THIS PART GOES UP WHILE SEEIONG THE OBSTACLE AND GOES FORWARD
    #WITH A TIME OUT
    thisTime = time.time()
    distance = tof.get_distance()
    while distance < 5000:
        print  "Distancia subiendo ", distance
        drone.moveUp(0.7)
        distance = tof.get_distance()
        actualTime = time.time()
        if (actualTime - thisTime) > 7 : 
            drone.land()
            print "TIME OUT"
            break
    print "FINISHED GOING UP"
    drone.moveUp(0.8)
    time.sleep(3)
    drone.hover()
    time.sleep(2)
    #THIS LANDS THE DRONE AFTER THE TIME OUT OR WHEN
    #IT DETECTS A WALL
    thisTime = time.time()
    distance = tof.get_distance()
    while distance > 1500:
        print "Distance: "
        distance = tof.get_distance()
        print distance
        if distance <  1501:
            drone.moveBackward(0.5)
        else:
            drone.moveForward(0.1)
        actualTime = time.time()
        if (actualTime - thisTime) > 3 : 
            drone.land()
            print "TIME OUT"
            break
 
    print "back"
    drone.moveBackward(0.5)
    time.sleep(0.5)
    drone.hover()
    time.sleep(1)

    print "land"
    drone.land()

if __name__ == "__main__":
    main()

