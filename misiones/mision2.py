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
    tof.start_ranging(4)
    time.sleep(0.001)
    if(tof.get_distance()==-1):
	print "No se inicializo correctamente el tof"
	return 	   
    print "Configuracion del drone"
    drone.startup()  # Connects to drone and starts subprocesses
    drone.reset()  # Always good, at start
    drone.trim()                                       # Recalibrate sensors
    #drone.getSelfRotation(5)
    time.sleep(0.5)
    thread.start()
    print "BATERIA ACTUAL: ", drone.getBattery()[0]

    #NAV DATA
    print "Obteniendo paquete de medidas"
    drone.useDemoMode(False)
    drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])


    print "Comienzo el programa"
    print "takeoff"
    drone.takeoff()
    time.sleep(2)
    drone.hover()
    time.sleep(2)
    #drone.setSpeed(0.1)
    print "hovering"
    
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
    time.sleep(5)

    distance = tof.get_distance()
    while distance<2500 and distance !=0:
        distance = tof.get_distance()
        print "Distance", distance
        if distance>2501:
            drone.stop()
        else:
            drone.moveLeft(0.1)
    print "Clear" 
    drone.stop()
    drone.moveRight(0.3)
    time.sleep(0.3)
    print "Stopped"
    '''
    #THIS PART GOES to the right until nothing is in front 

    NDC = drone.NavDataCount
    alti = 0.0
    while alti < 1400:
        while drone.NavDataCount == NDC:   time.sleep(0.001)
        NDC = drone.NavDataCount
        alti = drone.NavData["altitude"][3]
        print "Altitude: " + str(alti)
        drone.move(0,0.05,0.99,0.0)
    '''
    # #THIS PART GOES UP WHILE SEEIONG THE OBSTACLE AND GOES FORWARD
    # #WITH A TIME OUT
    # thisTime = time.time()
    # distance = tof.get_distance()
    # while distance < 5000:
    #     print  "Distancia subiendo ", distance
    #     drone.moveUp(0.7)
    #     distance = tof.get_distance()
    #     actualTime = time.time()
    #     if (actualTime - thisTime) > 7 : 
    #         drone.land()
    #         print "TIME OUT"
    #         break
    # print "FINISHED GOING UP"
    '''
    drone.moveDown(0.2)
    time.sleep(0.5)
    '''
    drone.hover()
    time.sleep(2)	

    #THIS LANDS THE DRONE AFTER THE TIME OUT OR WHEN
    #IT DETECTS A WALL
    thisTime = time.time()
    distance = tof.get_distance()
    print "Distance before while: ",distance
    while distance > 1000 or distance < 1:
        distance = tof.get_distance()
        print "Distance: ",distance
        if distance <  1001:
            drone.moveBackward(0.5)
        else:
            drone.moveForward(0.1)
        actualTime = time.time()
        if (actualTime - thisTime) > 6 : 
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

