import sys
sys.path.insert(0,"../")

import threading
import api.ps_drone as ps_drone
import time

class keyThread(threading.Thread):
	def __init__(self, drone):
		threading.Thread.__init__(self)
		self.drone = drone
		self.exit = False
	def run(self):
		while(not self.exit):
			if self.drone.getKey(): self.exit = True
		print "landing"
		self.drone.land()
		print "disconecting"
		self.drone.shutdown()

drone = ps_drone.Drone()  # Start using drone
thread = keyThread(drone)

drone.startup()  # Connects to drone and starts subprocesses
drone.reset()  # Always good, at start
drone.trim()
drone.getSelfRotation(5)
time.sleep(0.5)
thread.start()
print "Bateria: ", drone.getBattery()[0]
print "takeoff"
drone.takeoff()
time.sleep(2)

print "hovering"
drone.hover()
time.sleep(5000)


print "land"
drone.land()