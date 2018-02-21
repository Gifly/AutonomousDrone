

import api.ps_drone as ps_drone
import time


drone = ps_drone.Drone()  # Start using drone

drone.startup()  # Connects to drone and starts subprocesses
drone.reset()  # Always good, at start

time.sleep(0.5)

print "takeoff"
drone.takeoff()
time.sleep(5)

print "hovering"
drone.hover()
time.sleep(3)

drone.doggyWag()

print "hovering"
drone.hover()
time.sleep(3)

print "land"
drone.land()