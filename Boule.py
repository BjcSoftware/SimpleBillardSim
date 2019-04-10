from Vec2 import *
from enum import Enum

class Border(Enum):
	NoBorder = 0
	UpperBorder = 1
	LowerBorder = 2
	LeftBorder = 3
	RightBorder = 4

class Boule:
	def __init__(self, parent, pos, radius, mass):
		self._parent = parent

		self._totalForce = Vec2(0, 0)
		
		self._p = pos
		self._v = Vec2(0, 0)
		self._speed = self._v.getMagnitude()
		self._a = Vec2(0, 0)
		
		self._radius = radius
		self._m = mass
			
		self.color = "red"
		self.circle = None
		self._draw()
	
	def executeNextStepInSimulation(self, dt):
		self._totalForce = self._calculateTotalForce();
		
		self._a = self._totalForce/self._m
		
		dv = self._a*dt
		self._v += dv
		
		if self._speed < 0.001:
			self._v = Vec2(0, 0)
		
		self._speed = self._v.getMagnitude()
		
		dPos = self._v*dt
		self._p += dPos
		
		self._detectAndReactToCollisions()
		
		self._draw()
	
	def _calculateTotalForce(self):
		totalForce = Vec2(0, 0)
		
		# Force normale
		Fn = self._m * 9.81
		
		# Force de frottement
		Fk = self._calculateFrictionalForce(Fn)
		totalForce += Fk
		
		return totalForce
	
	def _calculateFrictionalForce(self, fn):
		# la force de frottement n'a d'effet que si la boule est en mouvement
		if self._speed != 0:
			uk = 0.03
			Fk = fn*uk
			frictionalForceDirection = self._v.normalize() * -1
			Fk = frictionalForceDirection * Fk
			return Fk
		else:
			return Vec2(0, 0)
	
	def _detectAndReactToCollisions(self):
		self._detectAndReactToCollisionsWithBorders()
		self._detectAndReactToCollisionsWithOtherBalls()
	
	def _detectAndReactToCollisionsWithBorders(self):
		border = self._checkForCollisionWithBorders()
		if border is not Border.NoBorder:
			self._reactToCollisionWithBorder(border)
	
	def _checkForCollisionWithBorders(self):
		if self._isCollidingWithUpperBorder():
			return Border.UpperBorder
		elif self._isCollidingWithLowerBorder():
			return Border.LowerBorder
		elif self._isCollidingWithLeftBorder():
			return Border.LeftBorder
		elif self._isCollidingWithRightBorder():
			return Border.RightBorder
		else:
			return Border.NoBorder
	
	def _isCollidingWithUpperBorder(self):
		ballIsCollidingWithTheBorder = self._p.y+self._radius >= self._parent._upperSideBorder
		ballIsGoingInBorderDirection = self._v.y > 0
		return ballIsCollidingWithTheBorder and ballIsGoingInBorderDirection
	
	def _isCollidingWithLowerBorder(self):
		ballIsCollidingWithTheBorder = self._p.y-self._radius <= self._parent._lowerSideBorder
		ballIsGoingInBorderDirection = self._v.y < 0
		return ballIsCollidingWithTheBorder and ballIsGoingInBorderDirection
	
	def _isCollidingWithLeftBorder(self):
		ballIsCollidingWithTheBorder = self._p.x-self._radius <= self._parent._leftSideBorder
		ballIsGoingInBorderDirection = self._v.x < 0
		return ballIsCollidingWithTheBorder and ballIsGoingInBorderDirection
	
	def _isCollidingWithRightBorder(self):
		ballIsCollidingWithTheBorder = self._p.x+self._radius >= self._parent._rightSideBorder
		ballIsGoingInBorderDirection = self._v.x > 0
		return ballIsCollidingWithTheBorder and ballIsGoingInBorderDirection
	
	def _reactToCollisionWithBorder(self, border):
		if border in (Border.UpperBorder, Border.LowerBorder):
			self._v.y *= -1
		elif border in (Border.RightBorder, Border.LeftBorder):
			self._v.x *= -1
	
	def _detectAndReactToCollisionsWithOtherBalls(self):
		for otherBall in self._parent.balls:
			if otherBall is not self:
				if self._isCollidingWithBall(otherBall):
					self._reactToCollisionWithBall(otherBall)
	
	def _isCollidingWithBall(self, otherBall):
		collisionDirection = (self.getPos() - otherBall.getPos()).normalize()
		relativeVelocity = (self.getVelocity() - otherBall.getVelocity()).dotproduct(collisionDirection)
		
		distanceBetweenBalls = self._getDistanceWithBall(otherBall)
		minDistanceBetweenBalls = self.getRadius() + otherBall.getRadius()
		if distanceBetweenBalls <= minDistanceBetweenBalls and relativeVelocity < 0:
			return True
		else:
			return False
	
	def _getDistanceWithBall(self, otherBall):
		vectorBetweenTheTwoBalls = self._p - otherBall.getPos()
		return vectorBetweenTheTwoBalls.getMagnitude()
	
	def _reactToCollisionWithBall(self, otherBall):	
		v1_initial = self.getVelocity()
		m1 = self.getMass()
		x1 = self.getPos()
		
		v2_initial = otherBall.getVelocity()
		m2 = otherBall.getMass()
		x2 = otherBall.getPos()
		
		v1_final = v1_initial - \
		(x1-x2) * (2*m2/(m1+m2)) * (((v1_initial - v2_initial).dotproduct(x1 - x2))/pow((x1 - x2).getMagnitude(), 2))
		
		v2_final = v2_initial - \
		(x2-x1) * (2*m1/(m1+m2)) * (((v2_initial - v1_initial).dotproduct(x2 - x1))/pow((x2 - x1).getMagnitude(), 2))
		
		
		self.setVelocity(v1_final)
		otherBall.setVelocity(v2_final)
	
	def _draw(self):
		posInPixels = self._parent.posInPixelsFromPosInMeters(self._p)
		
		if self._notDrawnYet():
			self._drawInitialBall(posInPixels)
		else:
			self._drawBallInNewLocation(posInPixels)
	
	def _notDrawnYet(self):
		return self.circle is None
	
	def _drawInitialBall(self, posInPixels):
		radiusInPixels = self._parent.metersToPixels(self._radius)
		self.circle = self._parent.create_oval(posInPixels.x - radiusInPixels,
							posInPixels.y-radiusInPixels,
							posInPixels.x+radiusInPixels,
							posInPixels.y+radiusInPixels,
							fill = self.color)
		
	
	def _drawBallInNewLocation(self, newPosInPixels):
		radiusInPixels = self._parent.metersToPixels(self._radius)
		self._parent.coords(self.circle, 
				newPosInPixels.x - radiusInPixels,
				newPosInPixels.y-radiusInPixels,
				newPosInPixels.x+radiusInPixels,
				newPosInPixels.y+radiusInPixels)
	
	def setVelocity(self, newVelocity):
		self._v = newVelocity
		self._speed = self._v.getMagnitude()
	
	def getVelocity(self):
		return self._v
	
	def getRadius(self):
		return self._radius
	
	def getMass(self):
		return self._m
	
	def getPos(self):
		return self._p
		
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		