import time
import sys
import cv2
sys.path.insert(0,"../")

import threading
import api.ps_drone as ps_drone

class keyThread(threading.Thread):
	def __init__(self, drone):
		threading.Thread.__init__(self)
		self.drone = drone
		self.exit = False
	def run(self):
		while(not self.exit):
			if self.drone.getKey(): self.exit = True
			time.sleep(0.1)

		print "landing"
		self.drone.land()
		print "disconecting"
		cv2.destroyAllWindows()
		self.drone.shutdown()
		self.terminate()