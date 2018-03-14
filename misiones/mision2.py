import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
import time
from vision import vision


def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage                 # Copy video-image
    pImg = cv2.resize(img,(640,360), interpolation = cv2.INTER_CUBIC)
    return img      # Returns image

def filterInd():
    values =[]
    total  0.0
    for i in range(0,5):
        values.append(vision.getKeypoints(getImage()))
    values.sort()
    for y in range(1,4):
        total = total+values[y]
    valorFin = total/3
    return valorFin

def main():

    print "Booting up the drone"
    drone = ps_drone.Drone()                                                    
    drone.startup()
    drone.reset()
    drone.trim()                                     
    drone.getSelfRotation(5) 
    drone.setConfigAllID()

    print "Booting up the camera"
    drone.frontCam()
    drone.hdVideo()
    drone.startVideo()
    CDC = drone.ConfigDataCount
    while CDC == drone.ConfigDataCount: time.sleep(0.0001)  # Wait until it is done (after resync is done)
    drone.startVideo()

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
