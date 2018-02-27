from turtle import *

def acc(self):
         a = Vec2D(0,0)
         for planet in self.gravSys.planets:

                if planet == self: continue
                r = planet.pos()-self.pos()
                a += (G*planet.m/abs(r)**3) * r
         return a

def step(self):
         sun = self.gravSys.planets[0]
         self.setpos(self.pos() + dt*self.v)
         if self != sun:
                  self.seth(self.towards(sun))
         self.a = self.acc()
         
self.v = self.v + dt*self.a
