import numpy as np
import random
import math


class city:
    
    def __init__(self,Ps,Pi,Pr,density,indice):
		self.indice=indice
                self.pop=   pop[i]
                self.S=int(Ps*self.pop)
		self.I=int(Pi*self.pop)
		self.R=int(Pr*self.pop)
		self.Psi=Psi
		self.Pir=Pir
		self.density=density
		self.area=(S+I+R)/density
		



		
"""					
    def run (self):
		for t in range(self.limiteTime):
			self.move()
			self.reproduce()
			self.rayon=math.sqrt(self.infectedSurface()/math.pi)
			print self.space
			print "Rayon d'infection=%f"%self.rayon
		self.export(self.fichier)
"""
		