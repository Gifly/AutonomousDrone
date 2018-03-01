import sys
sys.path.insert(0,"../")

import api.ps_drone as ps_drone
import time


drone = ps_drone.Drone()  # Start using drone

drone.startup()  # Connects to drone and starts subprocesses
drone.reset()  # Always good, at start
drone.trim()
drone.getSelfRotation(5)
time.sleep(0.5)

print "takeoff"
drone.takeoff()
time.sleep(2)

print "hovering"
drone.hover()
time.sleep(5)

print "land"
drone.land()
