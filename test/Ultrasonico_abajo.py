import sys
sys.path.insert(0,"../")
import time
import api.ps_drone as ps_drone

def main():

	drone = ps_drone.Drone()
	print "Configuracion del drone"
	drone.startup()  # Connects to drone and starts subprocesses
	drone.reset()  # Always good, at start
	drone.trim()  # Recalibrate sensors
	drone.getSelfRotation(5)
	time.sleep(0.5)
	print "BATERIA ACTUAL: ", drone.getBattery()[0]
	drone.useDemoMode(False)
	drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
	print "Obteniendo paquete de medidas"
	time.sleep(1.0)
	print "takeoff"
	drone.takeoff()
	time.sleep(2)
	drone.hover()
	time.sleep(3)


	stop = False
	NDC = drone.NavDataCount
	alti = 0.0
	rpm = 5000.0
	while alti < 2500:
		while drone.NavDataCount == NDC:   time.sleep(0.001)
		if drone.getKey(): 	stop = True
		NDC = drone.NavDataCount
		alti = drone.NavData["altitude"][3]
		print "Altitude: " + str(alti)
		print "RPM: " +str(rpm)
		drone.moveUp(1.0)
	drone.moveDown(0.6)
	time.sleep(1)
	drone.hover()
	time.sleep(1)
	print "land"
	drone.land(),

if __name__ == "__main__":
    main()