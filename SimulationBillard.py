from tkinter import *
from Table import *
from Vec2 import *
from Timer import *

class SimulationBillard:
	def __init__(self, dimTableInPixels):
		assert dimTableInPixels.x == 2*dimTableInPixels.y
	
		self.root = Tk()
		self.root.title("Simulation billard")

		self.dimTableInPixels = dimTableInPixels
		self._initTable()
		self._initBalls()
		
		self.timerBetweenUpdates = Timer()
	
	def start(self):
		self.timerBetweenUpdates.start()
		self.table.after(0, self._update)
		self.root.mainloop()
	
	def _initTable(self):
		dimTableInMeters = Vec2(3.1, 3.1/2)
		self.table = Table(self.root, dimTableInMeters, self.dimTableInPixels)
		
		self.table.pack()
	
	def	_initBalls(self):
		ballCount = 12
		for i in range(0, ballCount):
			self.table.addBall()
	
	def _update(self):
		dt = self.timerBetweenUpdates.getElapsedTimeAndRestart()
		self.table.executeNextStepInSimulation(dt)
		self.table.after(1, self._update)

if __name__ == "__main__":
	dimTableInPixels = Vec2(1000, 500)
	simulation = SimulationBillard(dimTableInPixels)
	simulation.start()















