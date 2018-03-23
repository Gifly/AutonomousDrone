import cv2
import sys
sys.path.insert(0,"../")
import api.ps_drone as ps_drone
from tools import emergency
from vision import vision
from PID import PIDrone
import time

drone = ps_drone.Drone()

def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage                 # Copy video-image
    pImg = cv2.resize(img,(640,360), interpolation = cv2.INTER_CUBIC)
    return img      # Returns image

def main():

      # Start using drone

    thread = emergency.keyThread(drone)
    print "Configuracion del drone"
    drone.startup()  # Connects to drone and starts subprocesses
    drone.reset()  # Always good, at start
    drone.trim()                                       # Recalibrate sensors
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
    print "BATERIA ACTUAL: ", drone.getBattery()[0]
    PIDx = PIDrone.DronePID(0.050, 0.02, 0)

    print "Comienzo el programa"

    time.sleep(0.001)
    drone.useDemoMode(False)
    drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
    time.sleep(1.0)

    print "takeoff"
    drone.takeoff()
    time.sleep(2)
    print "hovering"
    drone.hover()
    time.sleep(4)
    #drone.setSpeed(0.1)
   

    #GETS NEAR THE OBJECT
    vision.setRange()
    frame = getImage()
    coordX, coordY, area = vision.getCenter(frame)
    while coordY > -1 and coordY < 300 and area < 1001000:
        drone.moveForward(0.15)
        frame = getImage()
        coordX, coordY, area = vision.getCenter(frame)
        print coordX, coordY, area
    drone.moveBackward(0.2)
    time.sleep(1)


    #ALINENANDOSE CON EL OBJETO
    drone.hover()
    time.sleep(1)
    print "Alinenandose"
    initTime = time.time()
    while(time.time()< initTime + 2):
        frame = getImage()
        coordX, coordY, area = vision.getCenter(frame)
        if coordX != -1 and coordY !=-1:
            SpeedX = -1.0*PIDx.getVelocity(0.005,320,coordX)
            drone.move(SpeedX, 0.0, 0.0, 0.0)
            print SpeedX
        else:
            drone.hover()
            print "Not found again"
        
    drone.stop()
    time.sleep(1)


    print "Going up"

    #THIS PART GOES UP 1600 mm
    NDC = drone.NavDataCount
    alti = 0.0
    while alti < 1700:
        while drone.NavDataCount == NDC:   time.sleep(0.001)
        NDC = drone.NavDataCount
        alti = drone.NavData["altitude"][3]
        print "Altitude: " + str(alti)
        drone.move(0,-0.05,0.99,0.0)

    print "Done"
    drone.stopVideo()


    drone.moveDown(0.2)
    time.sleep(0.5)
    drone.hover()
    time.sleep(2)	

    print "FORWARD"
    drone.moveForward(0.2)
    time.sleep(2.5)

    drone.hover()
    time.sleep(2)
    print "land"
    drone.land()

if __name__ == "__main__":
    main()

