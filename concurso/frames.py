import sys
import cv2
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
from vision import vision
from tools import emergency
import time
Debug = True
drone = ps_drone.Drone()  # Start using drone
def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage 
    pImg = cv2.resize(img,(640, 360), interpolation = cv2.INTER_CUBIC)               
    return pImg 


def alinearVen(Direccion, frame, drone):
    Found = False
    timeIni = time.time()
    cantTime = 3.3
    timeOut = False
    while(not(Found) and not(timeOut)):
        frame =  getImage()
        timeOut = time.time() > timeIni + cantTime
        Found = vision.seeYellow(frame)
        if(Direccion):
            drone.moveRight(0.1)            #Moverse a la derecha
        else:
            drone.moveLeft(0.1)    
        #Moverse a la izquierda   
    time.sleep(0.08)
    if(timeOut):
        print "no lo encontre, timeOut"
    else:
        print "si lo encontre avanzo"
    
    drone.stop()
    if(Debug):
        print "Me detengo"
    time.sleep(3)
    return timeOut
        


def main():

    thread = emergency.keyThread(drone)
    print "Booting up the drone"
    drone.startup()
    drone.reset()
    drone.trim()                                     
    drone.getSelfRotation(5) 
    time.sleep(0.5)
    thread.start()

    #Drone's camera initial configuration
    print "Booting up the camera"
    drone.frontCam()
    drone.hdVideo()
    drone.startVideo()
    CDC = drone.ConfigDataCount
    while CDC == drone.ConfigDataCount: time.sleep(0.0001)  # Wait until it is done (after resync is done)
    drone.startVideo()
    
    time.sleep(0.001)
    print "Initial configuration complete"
    print 'BATTERY: ',drone.getBattery()[0]
    drone.useDemoMode(False)
    drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
    print "takeoff"
    drone.takeoff()
    time.sleep(3)
    drone.hover()
    time.sleep(2)
    vision.setRange()

    #Subir a 1.1 metros
    #THIS PART GOES UP 1600 mm
    NDC = drone.NavDataCount
    alti = 0.0
    while alti < 800:
        while drone.NavDataCount == NDC:   time.sleep(0.001)
        NDC = drone.NavDataCount
        alti = drone.NavData["altitude"][3]
        print "Altitude: " + str(alti)
        drone.moveUp(0.99)
        if(alti>1101):
            drone.moveDown(0.3)
            time.sleep(0.2)
    drone.hover()
    time.sleep(2)
    if(Debug):
        print "Altitud alcanzada"
    Direccion = True
    for i in range (0,4):

        drone.moveForward(0.1)
        time.sleep(2.7)
        drone.stop()
        time.sleep(1)
        frame = getImage()
        Direccion = (i % 2 ==0)
        if(Debug):
            print "Ventana actual: ", i
            print "Direccion"
            if(Direccion):
                print"Derecha"
            else:
                print "izquierda"
        timeOut = alinearVen(Direccion,frame, drone)
        if(timeOut):
            print
            #break
    print "Ya acabe las ventanas"
    if(not timeOut):
        drone.moveForward(0.1)
        time.sleep(1)
    drone.stop()
    drone.land()
    cv2.destroyAllWindows()

def maine():
   
    #thread = emergency.keyThread(drone)
    print "Configuracion del drone"
    drone.startup()  # Connects to drone and starts subprocesses
    drone.reset()  # Always good, at start
    drone.trim()                                       # Recalibrate sensors
    drone.getSelfRotation(5)
    drone.setConfigAllID()
    cap = cv2.VideoCapture(0)
    #Drone's camera initial configuration
    print "Booting up the camera"
    drone.frontCam()
    drone.hdVideo()
    drone.startVideo()
    time.sleep(0.5)
    #thread.start()
    print "BATERIA ACTUAL: ", drone.getBattery()[0]

    print "Comienzo el programa"
    vision.setRange()
    print "Yellow"
    frame = getImage()
    alinearVen(True,frame,drone)

if __name__ == "__main__":
    main()
