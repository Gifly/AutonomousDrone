import PID.PIDrone as PIDrone
import math

k_p = 1#1 Best sim value
k_i = 1#1 Best sim value
k_d = 0.0
sample_time = 0.01
run_time = 3.0
set_point = 320
velocity = 0.0
feedback = 0
drone = PIDrone.DronePID(k_p, k_i, k_d)
status = True
again = True
n = 0

while status:
	n = input("""Press the number for the correct menu option
	... 1. Set Propotional Control
	... 2. Set Integral Control
	... 3. Set Derivative control
	... 4. Set Setpoint
	... 5. Set Sample time in seconds
	... 6. Set run time in seconds
	... 7. Set starting offset
	... 8. Start simulation
	... 0. Exit program 
	""")
	if(n == 1):
		k_p = input("Write new proportional control value: ")
		drone.setKp(k_p)
	elif(n == 2):
		k_i = input("Write new integral control value: ")
		drone.setKi(k_i)
	elif(n == 3):
		k_d = input("Write new diferential control value: ")
		drone.setKi(k_d)
	elif(n == 4):
		set_point = input("Write new setpoint value: ")
		drone.setSetPoint(set_point)
	elif(n == 5):
		sample_time = input("Write new sample time value: ")
		drone.setSampleTime(sample_time)
	elif(n == 6):
		run_time = input("Write new run time value: ")
	elif(n == 7):
		feedback = input("Write new feedback value: ")
	elif(n == 8):
		for i in range(0, int(run_time/sample_time - 1)):
			velocity = drone.getVelocity(sample_time, set_point, feedback)
			feedback = int(velocity*2000*sample_time) + feedback
			print "pixel: " , feedback , " Velocidad: " , velocity , " Out " , drone.velocity
		feedback= 640
	elif(n == 0):
		status = False