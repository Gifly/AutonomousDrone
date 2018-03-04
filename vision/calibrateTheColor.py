import cv2
import numpy as np
import sys
import time
sys.path.insert(0, '../')
import api.ps_drone as ps_drone



def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage 
    pImg = cv2.resize(img,(640, 360), interpolation = cv2.INTER_CUBIC)               
    return pImg      # Returns image

print "Booting up the drone for color calibration"
drone = ps_drone.Drone()                                                    
drone.startup()
drone.reset()
drone.trim()                                     
drone.getSelfRotation(5) 
drone.setConfigAllID()
#Drone's camera initial configuration
print "Booting up the camera"
drone.frontCam()
drone.hdVideo()
drone.startVideo()
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount: time.sleep(0.0001)  # Wait until it is done (after resync is done)
drone.startVideo()

cv2.namedWindow('HSV', cv2.WINDOW_NORMAL)
cv2.resizeWindow('HSV', 290, 300)
file = open("colorVal.txt","r")
lowVal=[]
uppVal=[]
i=0
for line in file:
    print line
    if(i<3):
        lowVal.append(int(line))
    else:
        uppVal.append(int(line))
    i+=1
file.close()
def nothing(x):
    pass


# create trackbars for color change
cv2.createTrackbar('HL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('SL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('VL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('HU', 'HSV', 255, 255, nothing)
cv2.createTrackbar('SU', 'HSV', 255, 255, nothing)
cv2.createTrackbar('VU', 'HSV', 255, 255, nothing)
cv2.createTrackbar('SAVE', 'HSV',0,1,nothing)

hl = cv2.setTrackbarPos('HL', 'HSV',lowVal[0])
sl = cv2.setTrackbarPos('SL', 'HSV',lowVal[1])
vl = cv2.setTrackbarPos('VL', 'HSV',lowVal[2])
hu = cv2.setTrackbarPos('HU', 'HSV',uppVal[0])
su = cv2.setTrackbarPos('SU', 'HSV',uppVal[1])
vu = cv2.setTrackbarPos('VU', 'HSV',uppVal[2])
save = cv2.setTrackbarPos('SAVE', 'HSV',0)
k = 0
while k != 27:

    # Take each frame
    frame = getImage()
    lowVal[0] = cv2.getTrackbarPos('HL', 'HSV')
    lowVal[1] = cv2.getTrackbarPos('SL', 'HSV')
    lowVal[2] = cv2.getTrackbarPos('VL', 'HSV')
    uppVal[0] = cv2.getTrackbarPos('HU', 'HSV')
    uppVal[1] = cv2.getTrackbarPos('SU', 'HSV')
    uppVal[2] = cv2.getTrackbarPos('VU', 'HSV')
    saveStatus = cv2.getTrackbarPos('SAVE','HSV')

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range
    lower = np.array([lowVal[0],lowVal[1], lowVal[2]])
    upper = np.array([uppVal[0], uppVal[1], uppVal[2]])

    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    if(saveStatus==1):
        font = cv2.FONT_ITALIC
        file=open("colorVal.txt","w")
        file.write(str(lowVal[0]) + "\n")
        file.write(str(lowVal[1]) + "\n")
        file.write(str(lowVal[2]) + "\n")
        file.write(str(uppVal[0]) + "\n")
        file.write(str(uppVal[1]) + "\n")
        file.write(str(uppVal[2]) + "\n")
        cv2.putText(res,'Valor Guardado',(50,50),font,1,(255,255,255),2)
        file.close()

    cv2.imshow('res',res)
    cv2.imshow('original', frame)
    k = cv2.waitKey(5)

cv2.destroyAllWindows()
