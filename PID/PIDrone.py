# Title: PID0
# Description: PID controller for the AR Drone 2.0 based on ivPID by Caner Durmusoglu 
# Author: Christian Bentin
# Date: 22-02-2018
# ============================================================================================
from ivPID import PID 


class DronePID(PID.PID):

	def __init__(self, P, I, D):
		PID.PID.__init__(self, P, I, D)
		self.velocity = 0.0

	def setSetPoint(self, SetPoint):
		self.SetPoint = SetPoint

	def getVelocity(self, sample_time, setpoint, feedback):
		self.setSampleTime(sample_time)
		self.setSetPoint(setpoint)
		self.setWindup(0.8)
		self.velocity = self.update(feedback)/100
		if(self.velocity > 0.1):
			self.velocity = 0.1
		elif(self.velocity < -0.1):
			self.velocity = -0.1
		#elif(self.velocity<0.045 and self.velocity >=0):
			#self.velocity=0.0
		#elif(self.velocity>-0.045 and self.velocity <=0):
			#self.velocity=0.0
		return self.velocity
