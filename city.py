import numpy as np
import random
import math


class city:
    
    def __init__(self,field):     
    
        with open(field,'rb') as file:
            contents = csv.reader(file)
            pop = list()
            for row in contents:
                pop.append(row)        
                
            for i in xrange(0,3):
                pop.pop(0)
                pop.pop(-1)
            pop.pop(0)
            #Faut-il fermer le fichier
            
            self.nom=pop[0]
            self.indice=pop[1]
            self.population=pop[3]
            self.S=self.population
            self.I=[0]*len(self.population)
            self.R=[0]*len(self.population)
            self.density=self.pop[5]
            self.area=(self.S+self.I+self.R)/self.density

    def infection(self):
        for i in xrange(len(self.population)):
            print i
            R[i]=R[i]+int(simulation.Pir*I[i])
            I[i]=I[i]-int(simulation.Pir*I[i])+int(simulation.Psi*S[i])
            S[i]=S[i]-int(simulation.Psi*S[i])
		
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





