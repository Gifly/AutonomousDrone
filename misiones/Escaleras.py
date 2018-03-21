import VL53L0X
import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
from tools import emergency
import time

def main():

    drone = ps_drone.Drone()  # Start using drone
    tof = VL53L0X.VL53L0X()
    thread = emergency.keyThread(drone)
    print "Configuracion del drone"
    drone.startup()  # Connects to drone and starts subprocesses
    drone.reset()  # Always good, at start
    drone.trim()                                       # Recalibrate sensors
    #drone.getSelfRotation(5)
    time.sleep(0.5)
    thread.start()
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
    drone.useDemoMode(False)
    drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
    time.sleep(1.0)
    #THIS PART GETS NEAR THE OBSTACLE
    for i in range(0,2):
        distance = tof.get_distance()
        if i == 0:
		target = 1000
	else:
		target = 600        
        while distance > target:
            print "Distance: "
            distance = tof.get_distance()
            print distance
            if distance <= target:
                drone.moveBackward(0.5)
            else:
                drone.move(0.02,0.1,0.0,0.0)
            print "next"
        #time.sleep(3)
        print "back"
        drone.moveBackward(0.5)
        time.sleep(0.5)
        drone.hover()
        time.sleep(2)

        #THIS PART GOES UP 1.2 METERS USING DRONES INTEGRATED ULTRASONIC SENSOR
        NDC = drone.NavDataCount
        alti = 0.0
        while alti < 1100:
            while drone.NavDataCount == NDC:   time.sleep(0.001)
            if drone.getKey():  stop = True
            NDC = drone.NavDataCount
            alti = drone.NavData["altitude"][3]
            print "Altitude: " + str(alti)
            drone.move(0.00,0.02,0.6,0.0)  
    drone.hover()
    time.sleep(2)
    drone.moveLeft(0.3)
    time.sleep(2)
    drone.hover()
    time.sleep(2)
    drone.land()


if __name__ == "__main__":
    main()
