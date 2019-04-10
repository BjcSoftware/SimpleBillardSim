from math import *

class Vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __str__(self):
		return "({0}; {1})".format(self.x, self.y)
	
	def __add__(self, other):
		return Vec2(self.x+other.x, self.y+other.y)
	
	def __iadd__(self, other):
		self = self + other
		return self
	
	def __sub__(self, other):
		return Vec2(self.x-other.x, self.y-other.y)
		
	def __isub__(self, other):
		self = self - other
		return self
		
	def __mul__(self, other):
		if type(other) == type(1) or type(other) == type(1.0):
			return Vec2(self.x*other, self.y*other)
		else:
			return Vec2(self.x*other.x, self.y*other.y)
	
	def __imul__(self, other):
		return self*other
	
	def __truediv__(self, other):
		if type(other) == type(1) or type(other) == type(1.0):
			return Vec2(self.x/other, self.y/other)
		else:
			return Vec2(self.x/other.x, self.y/other.y)
	
	def getMagnitude(self):
		return sqrt(pow(self.x, 2) + pow(self.y, 2))
	
	def normalize(self):
		return self/self.getMagnitude()
		
	def dotproduct(self, other):
		return self.x*other.x + self.y*other.y