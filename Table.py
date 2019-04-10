from tkinter import *
from Boule import *
import random

class Table(Canvas):
	def __init__(self, parent, dimTableInMeters, dimTableInPixels):
		assert dimTableInMeters.x == 2*dimTableInMeters.y
		assert dimTableInPixels.x == 2*dimTableInPixels.y
		
		super().__init__(parent, width = dimTableInPixels.x, height = dimTableInPixels.y, bg = "green")
		self.dimTableInMeters = dimTableInMeters
		self.dimTableInPixels = dimTableInPixels
		self.balls = []
		
		self._upperSideBorder = self.dimTableInMeters.y
		self._rightSideBorder = self.dimTableInMeters.x
		self._lowerSideBorder = 0
		self._leftSideBorder = 0
		
	def getTableDimInMeters(self):
		return self.dimTableInMeters
	
	def addBall(self, pos = None, v = None):
		
		ballRadius = 0.0615
		ballMass = 0.210
	
		# Générer une position aléatoire sur la table
		if(pos == None):
			pos = Vec2(random.uniform(ballRadius, self.dimTableInMeters.x-ballRadius), 
					   random.uniform(ballRadius, self.dimTableInMeters.y-ballRadius))
		
		# Générer une vitesse initiale aléatoire
		if(v == None):
			v = Vec2(random.uniform(0, 4), random.uniform(0, 4))
			# v = Vec2(5, 5)
			
		newBall = Boule(self, pos, ballRadius, ballMass)
		newBall.setVelocity(v)
		self.balls.append(newBall)
	
	def posInPixelsFromPosInMeters(self, posInMeters):
		xInPixels = self.metersToPixels(posInMeters.x)
		
		# l'origine en pixels se trouve en haut à gauche de l'écran
		yInPixels = self.dimTableInPixels.y - self.metersToPixels(posInMeters.y)
		
		return Vec2(xInPixels, yInPixels)
	
	def metersToPixels(self, meters):
		metersPixelsRatio = self.dimTableInPixels.x/self.dimTableInMeters.x
		return meters*metersPixelsRatio
	
	def executeNextStepInSimulation(self, dt):
		for ball in self.balls:
			ball.executeNextStepInSimulation(dt)