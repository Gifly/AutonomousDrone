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
	
	'''
	CDC = drone.ConfigDataCount
	while CDC == drone.ConfigDataCount: time.sleep(0.0001)  # Wait until it is done (after resync is done)
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
	
	'''
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

	while alti < 1600:
		while drone.NavDataCount == NDC:   time.sleep(0.001)
		if drone.getKey(): 	stop = True
		NDC = drone.NavDataCount
		alti = drone.NavData["altitude"][3]
		print "Altitude: " + str(alti)
		drone.moveUp(0.9)
	drone.moveDown(0.6)
	time.sleep(1)
	drone.hover()
	time.sleep(1)
	print "land"
	drone.land()

if __name__ == "__main__":
    main()
