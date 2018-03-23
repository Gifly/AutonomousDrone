import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
#from tools import emergency
import time

def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage 
    pImg = cv2.resize(img,(640, 360), interpolation = cv2.INTER_CUBIC)               
    return pImg 


def alinearVen(Direccion, frame, drone):
    Found = False
    timeIni = time.time()
    cantTime = 5
    timeOut = False
    while(Found or not(timeOut)):
        frame =  getImage()
        timeOut = time.time() > timeIni + cantTime
        Found = vision.seeYellow(frame)
        if(Direccion):
            drone.moveRight(0.08)            #Moverse a la derecha
        else:
            drone.moveLeft(0.08)    
        #Moverse a la izquierda    
    if(timeOut):
        print "no lo encontre, timeOut"
    else:
        print "si lo encontre avanzo"
    time.sleep(0.5)
    drone.stop()
    time.sleep(1)
    return timeOut
        


def main():

    drone = ps_drone.Drone()  # Start using drone
    #thread = emergency.keyThread(drone)
    print "Configuracion del drone"
    drone.startup()  # Connects to drone and starts subprocesses
    drone.reset()  # Always good, at start
    drone.trim()                                       # Recalibrate sensors
    drone.getSelfRotation(5)
    time.sleep(0.5)
    #thread.start()
    print "BATERIA ACTUAL: ", drone.getBattery()[0]

    print "Comienzo el programa"
    print "takeoff"
    drone.takeoff()
    time.sleep(3)
    drone.hover()
    time.sleep(2)
    #Subir a 1.1 metros
    Direccion = True
    for i in range (0,4):
        drone.moveForward(0.1)
        time.sleep(1)
        drone.stop()
        time.sleep(1)
        frame = getImage()
        Direccion = (i % 2 ==0)
        timeOut = alinearVen(Direccion,frame, drone)
        if(timeOut):
            break

    if(not timeOut):
        drone.moveForward(0.1)
        time.sleep(1)
    drone.stop()
    drone.land()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
