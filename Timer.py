import time

class Timer:
	def __init__(self):
		self.isStarted = False

	def start(self):
		self.isStarted = True
		self.timeWhenTimerStarts = time.perf_counter()
		
	def getElapsedTime(self):
		if self.isStarted:
			currentTime = time.perf_counter()
			elapsedTime = currentTime - self.timeWhenTimerStarts
			return elapsedTime
			
	def getElapsedTimeAndRestart(self):
		elapsedTime = self.getElapsedTime()
		self.start()
		return elapsedTime