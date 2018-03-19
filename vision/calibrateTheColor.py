import cv2
import numpy as np
import sys
import time
import vision
sys.path.insert(0, '../')
import api.ps_drone as ps_drone

def isCircle(cnt):
    template = cv2.imread('images/circle.jpg',0)
    ret, thresh = cv2.threshold(template, 127, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    match = cv2.matchShapes(contours[0], cnt, 1, 0.0)

    if match < 0.5:
        return True
    return False

def getImage():
    IMC = drone.VideoImageCount 
    while drone.VideoImageCount==IMC: time.sleep(0.01)  # Wait until the next video-frame
    img  = drone.VideoImage 
    pImg = cv2.resize(img,(640, 360), interpolation = cv2.INTER_CUBIC)               
    return pImg      # Returns image

def isRectangle(cnt):
    template = cv2.imread('../vision/images/rectangle.png',0)
    ret, thresh = cv2.threshold(template, 127, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    match = cv2.matchShapes(contours[0], cnt, 1, 0.0)

    if match < 0.30:
        return True
    return False


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
cv2.namedWindow('WINDOWS', cv2.WINDOW_NORMAL)
cv2.resizeWindow('HSV', 290, 300)
cv2.resizeWindow('WINDOWS', 290, 300)
file = open("colorVal.txt","r")
lowVal=[]
uppVal=[]
lowValInd = []
uppValInd =[]
lowValVen=[]
uppValVen=[]
kernel = np.ones((5,5), np.uint8)

i=0
for line in file:
    print line
    if(i<3):
        lowVal.append(int(line))
    elif(i<6):
        uppVal.append(int(line))
    elif(i<9):
        lowValInd.append(int(line))
    elif(i<12):
        uppValInd.append(int(line))
    elif(i<15):
        lowValVen.append(int(line))
    elif(i<18):
        uppValVen.append(int(line))
    i+=1
file.close()
def nothing(x):
    pass

print ""
# create trackbars for color change
cv2.createTrackbar('HL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('SL', 'HSV', 0, 255, nothing)
cv2.createTrackbar('VL', 'HSV', 0, 255, nothing)

cv2.createTrackbar('HU', 'HSV', 255, 255, nothing)
cv2.createTrackbar('SU', 'HSV', 255, 255, nothing)
cv2.createTrackbar('VU', 'HSV', 255, 255, nothing)

cv2.createTrackbar('HInd', 'HSV', 255, 255, nothing)
cv2.createTrackbar('SInd', 'HSV', 255, 255, nothing)
cv2.createTrackbar('VInd', 'HSV', 255, 255, nothing)

cv2.createTrackbar('HIUP', 'HSV', 255, 255, nothing)
cv2.createTrackbar('SIUP', 'HSV', 255, 255, nothing)
cv2.createTrackbar('VIUP', 'HSV', 255, 255, nothing)

cv2.createTrackbar('HVL', 'WINDOWS', 0, 255, nothing)
cv2.createTrackbar('SVL', 'WINDOWS', 0, 255, nothing)
cv2.createTrackbar('VVL', 'WINDOWS', 0, 255, nothing)

cv2.createTrackbar('HVU', 'WINDOWS', 255, 255, nothing)
cv2.createTrackbar('SVU', 'WINDOWS', 255, 255, nothing)
cv2.createTrackbar('VVU', 'WINDOWS', 255, 255, nothing)

cv2.createTrackbar('SAVE', 'HSV',0,1,nothing)

hl = cv2.setTrackbarPos('HL', 'HSV',lowVal[0])
sl = cv2.setTrackbarPos('SL', 'HSV',lowVal[1])
vl = cv2.setTrackbarPos('VL', 'HSV',lowVal[2])

hu = cv2.setTrackbarPos('HU', 'HSV',uppVal[0])
su = cv2.setTrackbarPos('SU', 'HSV',uppVal[1])
vu = cv2.setTrackbarPos('VU', 'HSV',uppVal[2])

HInd = cv2.setTrackbarPos('HInd', 'HSV',lowValInd[0])
SInd = cv2.setTrackbarPos('SInd', 'HSV',lowValInd[1])
VInd = cv2.setTrackbarPos('VInd', 'HSV',lowValInd[2])

HIUP = cv2.setTrackbarPos('HIUP', 'HSV',uppValInd[0])
SIUP = cv2.setTrackbarPos('SIUP', 'HSV',uppValInd[1])
VIUP = cv2.setTrackbarPos('VIUP', 'HSV',uppValInd[2])

HVL = cv2.createTrackbar('HVL', 'WINDOWS', 0, 255, lowValVen[0])
SVL = cv2.createTrackbar('SVL', 'WINDOWS', 0, 255, lowValVen[1])
VVL = cv2.createTrackbar('VVL', 'WINDOWS', 0, 255, lowValVen[2])

HVU = cv2.createTrackbar('HVU', 'WINDOWS', 255, 255, uppValVen[0])
SVU = cv2.createTrackbar('SVU', 'WINDOWS', 255, 255, uppValVen[1])
VVU = cv2.createTrackbar('VVU', 'WINDOWS', 255, 255, uppValVen[2])

save = cv2.setTrackbarPos('SAVE', 'HSV',0)
k = 0
while k != 27:
    Puntos =[]
    Ventanas = []
    # define range
    lower = np.array([lowVal[0],lowVal[1], lowVal[2]])
    upper = np.array([uppVal[0], uppVal[1], uppVal[2]])
    lowerInd = np.array ([lowValInd[0],lowValInd[1],lowValInd[2]])
    upperInd = np.array([uppValInd[0],uppValInd[1],uppValInd[2]])
    lowerWindow = np.array ([lowValVen[0],lowValVen[1],lowValVen[2]])
    upperWindow = np.array([uppValVen[0],uppValVen[1],uppValVen[2]])
    # Take each frame
    frame = getImage()
    
    lowVal[0] = cv2.getTrackbarPos('HL', 'HSV')
    lowVal[1] = cv2.getTrackbarPos('SL', 'HSV')
    lowVal[2] = cv2.getTrackbarPos('VL', 'HSV')
    
    uppVal[0] = cv2.getTrackbarPos('HU', 'HSV')
    uppVal[1] = cv2.getTrackbarPos('SU', 'HSV')
    uppVal[2] = cv2.getTrackbarPos('VU', 'HSV')
    
    lowValInd[0] = cv2.getTrackbarPos('HInd', 'HSV')
    lowValInd[1] = cv2.getTrackbarPos('SInd', 'HSV')
    lowValInd[2] = cv2.getTrackbarPos('VInd', 'HSV')

    uppValInd[0] = cv2.getTrackbarPos('HIUP', 'HSV')
    uppValInd[1] = cv2.getTrackbarPos('SIUP', 'HSV')
    uppValInd[2] = cv2.getTrackbarPos('VIUP', 'HSV')

    lowValVen[0] = cv2.getTrackbarPos('HVL', 'WINDOWS')
    lowValVen[1] = cv2.getTrackbarPos('SVL', 'WINDOWS')
    lowValVen[2] = cv2.getTrackbarPos('VVL', 'WINDOWS')

    uppValVen[0] = cv2.getTrackbarPos('HVU', 'WINDOWS')
    uppValVen[1] = cv2.getTrackbarPos('SVU', 'WINDOWS')
    uppValVen[2] = cv2.getTrackbarPos('VVU', 'WINDOWS')
    saveStatus = cv2.getTrackbarPos('SAVE','HSV')

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image
    mask = cv2.inRange(hsv, lower, upper)
    maskInd = cv2.inRange(hsv,lowerInd,upperInd)
    maskInd = cv2.morphologyEx(maskInd,cv2.MORPH_OPEN,kernel)
    maskVen = cv2.inRange(hsv,lowerInd,upperInd)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.bitwise_and(res, res, mask=maskVen)
    #Get contoursq
    contours , hierarchy = cv2.findContours(maskInd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contoursV , hierarchyV = cv2.findContours(maskVen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #Indicators
    n = len(contours)
    contours = sorted(contours,key=cv2.contourArea, reverse=True)[:n]
    print len(contours)
    if(len(contours)>=2):
        for i in range (0,2):
            if(isCircle(contours[i])):
                Puntos.append(contours[i])
        
    if(Puntos):
        cv2.drawContours(res,Puntos,-1,(0,255,0),2)

    #Ventanas
    n = len(contoursV)
    contoursV = sorted(contoursV,key=cv2.contourArea, reverse=True)[:n]
    print len(contoursV)
    if(len(contoursV)>=1):
        if(isRectangle(contours[0])):
            Ventanas.append(contours[0])
        
    if(Ventanas):
        cv2.drawContours(res,Ventanas,-1,(0,100,100),2)

    if(saveStatus==1):
        font = cv2.FONT_ITALIC
        file=open("colorVal.txt","w")
        file.write(str(lowVal[0]) + "\n")
        file.write(str(lowVal[1]) + "\n")
        file.write(str(lowVal[2]) + "\n")

        file.write(str(uppVal[0]) + "\n")
        file.write(str(uppVal[1]) + "\n")
        file.write(str(uppVal[2]) + "\n")

        file.write(str(lowValInd[0]) + "\n")
        file.write(str(lowValInd[1]) + "\n")
        file.write(str(lowValInd[2]) + "\n")
        
        file.write(str(uppValInd[0]) + "\n")
        file.write(str(uppValInd[1]) + "\n")
        file.write(str(uppValInd[2]) + "\n")

        file.write(str(lowValVen[0]) + "\n")
        file.write(str(lowValVen[1]) + "\n")
        file.write(str(lowValVen[2]) + "\n")
        
        file.write(str(lowValVen[0]) + "\n")
        file.write(str(lowValVen[1]) + "\n")
        file.write(str(lowValVen[2]) + "\n")


        cv2.putText(res,'Valor Guardado',(50,50),font,1,(255,255,255),2)
        file.close()
    
    cv2.imshow('res',res)
    cv2.imshow('original', frame)
    k = cv2.waitKey(5)%256

cv2.destroyAllWindows()
