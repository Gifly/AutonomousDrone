import sys
sys.path.insert(0,"../")

import api.ps_drone as ps_drone
import time
print "Booting up the drone for sensor calibration"
drone = ps_drone.Drone()                                                    
drone.startup()
drone.reset()
drone.trim()                                     
drone.getSelfRotation(5) 
#drone.setConfigAllID()
#drone.getConfig()
#Drone's camera initial configuration
CDC = drone.ConfigDataCount
#while CDC == drone.ConfigDataCount: time.sleep(0.0001)  # Wait until it is done (after resync is done)
for i in drone.ConfigData:
	if i[0]== "control:euler_angle_max" or i[0]== "control:control_vz_max" or i[0]== "control:control_yaw":
		print str(i)
drone.setConfig("control:euler_angle_max","0.208")
drone.setConfig("control:control_vz_max","800")
drone.setConfig("control:control_yaw","1.75")
while CDC == drone.ConfigDataCount: time.sleep(0.15)
for i in drone.ConfigData:
	if i[0]== "control:euler_angle_max" or i[0]== "control:control_vz_max" or i[0]== "control:control_yaw":
		print str(i)
print "Bateria: ", drone.getBattery()[0]

print "takeoff"
drone.takeoff()
time.sleep(2)

print "hovering"
drone.hover()
time.sleep(5)

print "GOing up"
drone.moveUp(0.9)
time.sleep(3)

print "land"
drone.land()
