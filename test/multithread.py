import sys
sys.path.insert(0,"../")

import threading
import api.ps_drone as ps_drone
import time

class keyThread(threading, Thread):

	def __init__(self):
		threading.Thread.__init__(self)
	def run(self, drone):
		exit = false
		while(not exit):
			if drone.getkey: exit = true
		print "landing"
		dron.land

drone = ps_drone.Drone()  # Start using drone
thread = keyThread()

drone.startup()  # Connects to drone and starts subprocesses
drone.reset()  # Always good, at start
drone.trim()
drone.getSelfRotation(5)
time.sleep(0.5)
thread.run(drone)
print "Bateria: ", drone.getBattery()[0]
print "takeoff"
drone.takeoff()
time.sleep(2)

print "hovering"
drone.hover()
time.sleep(5000)


print "land"
drone.land()