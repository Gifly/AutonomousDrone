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
<<<<<<< HEAD
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
=======
    tof.start_ranging(4)
    time.sleep(0.001)
    #THIS PART GETS NEAR THE OBSTACLE
    distance = tof.get_distance()
    while distance > 900:
        print "Distance: "
        distance = tof.get_distance()
        print distance
        if distance < 901:
            drone.moveBackward(0.5)
        else:
            drone.moveForward(0.15)
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
    while distance < 8000:
        print  "Distancia subiendo ", distance
        drone.moveUp(0.5)
        distance = tof.get_distance()
        actualTime = time.time()
        if (actualTime - thisTime) > 7 : 
            drone.land()
            print "TIME OUT"
            break
    print "FINISHED GOING UP"
    #THIS LANDS THE DRONE AFTER THE TIME OUT OR WHEN
    #IT DETECTS A WALL
    thisTime = time.time()
    distance = tof.get_distance()
    while distance > 900:
        print "Distance: "
        distance = tof.get_distance()
        print distance
        if distance <  901:
            drone.moveBackward(0.5)
        else:
            drone.moveForward(0.15)
        actualTime = time.time()
        if (actualTime - thisTime) > 4 : 
            drone.land()
            print "TIME OUT"
            break
 
    print "back"
    drone.moveBackward(0.5)
    time.sleep(0.5)
    drone.hover()
    time.sleep(1)
>>>>>>> 952fe3e08443433b35ec4edd8953475be0b3e418

    print "land"
    drone.land()

if __name__ == "__main__":
    main()
