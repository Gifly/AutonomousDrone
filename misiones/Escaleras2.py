# import VL53L0X
import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
from tools import emergency
import time

def main():

    drone = ps_drone.Drone()  # Start using drone
    # tof = VL53L0X.VL53L0X()
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
    # tof.start_ranging(4)
    time.sleep(0.001)
    drone.useDemoMode(False)
    drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
    time.sleep(1.0)
    '''
    #THIS PART GETS NEAR THE OBSTACLE
    distance = tof.get_distance()
    print "Distance before while: ",distance
    while distance > 1300 and distance!=0:
        distance = tof.get_distance()
        print "Distance: ", distance
        if distance < 1301:
            drone.moveBackward(0.5)
        else:
            drone.moveForward(0.1)
        print "next"
    #time.sleep(3)
    print "back"
    drone.moveBackward(0.5)
    time.sleep(0.5)
    print "hover"
    drone.hover()
    time.sleep(3)
    '''

    drone.moveForward(0.1)
    time.sleep(2)
    drone.hover()
    time.sleep(1)
    for i in range(0,2):
        #THIS PART GOES UP 1600 mm
        NDC = drone.NavDataCount
        alti = 0.0
        while alti < 1100:
            while drone.NavDataCount == NDC:   time.sleep(0.001)
            NDC = drone.NavDataCount
            alti = drone.NavData["altitude"][3]
            print "Altitude UP: " + str(alti)
            drone.move(0,-0.03,0.6,0.0)

        drone.moveDown(0.2)
        time.sleep(0.5)
        drone.hover()
        time.sleep(1)

        NDC = drone.NavDataCount
        while alti > 800:
            while drone.NavDataCount == NDC:   time.sleep(0.001)
            NDC = drone.NavDataCount
            alti = drone.NavData["altitude"][3]
            print "Altitude FORWARD: " + str(alti)
            drone.move(0.0,0.07,0.0,0.0)
        print "back"
        drone.moveBackward(0.1)
        time.sleep(0.5)
        drone.hover()
        time.sleep(2)

    print "hover"
    drone.hover()
    time.sleep(2)
    print "left"
    drone.moveForward(0.2)
    # drone.moveLeft(0.2)
    time.sleep(1)
    drone.hover()
    time.sleep(2)
    print "land"
    drone.land()


if __name__ == "__main__":
    main()
