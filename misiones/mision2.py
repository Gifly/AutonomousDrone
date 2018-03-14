import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time
from vision import vision

def filterInd():
    values =[]
    total  0.0
    for i in range(0,5):
        values.append(getKeypoints())
    values.sort()
    for y in range(1,4):
        total = total+values[y]
    valorFin = total/3
    return valorFin


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
    indMin = 1000
    print "Comienzo el programa"
    print "takeoff"
    drone.takeoff()
    time.sleep(2)
    drone.hover()
    time.sleep(2)
    print "hovering"
    k=0
    finalized=False
    while k!=27 or not(finalized) :
        k =cv2.waitKey(5)%256
        drone.moveForward()
        measuresPass=0
        if(filterInd()>indMin):
            drone.hover()
            for i in range(0,3):
                if(filterInd()>indMin):
                    measuresPass+=1
                    print "Distance achieved", measuresPass
        finalized = (measuresPass==3)          

    print "land"
    drone.land()

if __name__ == "__main__":
    main()
