import numpy as np
import random
import math
import csv
#import simulation

class worldCities:
    
    def __init__(self,field):     
				
				##### Recuperation des donnees des villes #####
        with open(field,'rb') as file: #Lecture du fichier
            contents = csv.reader(file)
            pop = list()
            for row in contents:
								pop.append(row)        
                
            for i in xrange(0,3): #Supprimer les 4 premieres et 3 dernieres lignes
                pop.pop(0)
                pop.pop(-1)
            pop.pop(0)

            for i in xrange(len(pop)): #Separation du tableau pop
							for j in xrange(1,6):
								pop[i].append(float(pop[i][0].split(";")[j]))
							pop[i].append(pop[i][0].split(";")[6])
							pop[i][0]=pop[i][0].split(";")[0]
							#Faut-il fermer le fichier

						#Creation de tableaux de noms
            self.name=[]
            self.indice=[]
            self.population=[]
            self.S=[]
            self.I=[]
            self.R=[]
            self.density=[]
            self.area=[]
            for i in xrange(len(pop)):
							self.name.append(pop[i][0])
							self.indice.append(pop[i][1])
							self.population.append(pop[i][3])
							self.S.append(self.population[i])
							self.I.append(0)
							self.R.append(0)
							self.density.append(pop[i][5])
							self.area.append((self.S[i]+self.I[i]+self.R[i])/self.density[i]) #Peut etre inutile
							print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]

		##### Classe d'infection des populations au sein d'une meme ville, sans echange #####
    def infection(self,Psi,Pir,iterations):
			for j in xrange(iterations):
				print "CONTAMINATION NUMBER ",j+1
				for i in xrange(len(self.population)):
						self.R[i]=self.R[i]+(Pir*self.I[i])//1
						self.I[i]=self.I[i]-(Pir*self.I[i])//1+(Psi*self.S[i])//1
						self.S[i]=self.S[i]-(Psi*self.S[i])//1
						print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]


"""	Extrait du SIR fait en TP en debut d'annee "			
    def run (self):
		for t in range(self.limiteTime):
			self.move()
			self.reproduce()
			self.rayon=math.sqrt(self.infectedSurface()/math.pi)
			print self.space
			print "Rayon d'infection=%f"%self.rayon
		self.export(self.fichier)
"""


#J'aurais bien aime que ceci soit sur le fichier simulation.py, faire plusieurs
#classes pour lancer le programme mais je n'ai pas reussi a faire le lien entre les
#classes car une city doit etre creee dans simulation tout en utilisant les variables
#de simulation...

class simulation:
    
    def __init__(self,field):

        ##### Import parameters #####
        with open(field,'r') as f:
            content = f.readlines()
            for i in range(len(content)):
                content[i]=content[i].split("\t")[0]
            self.Psi=float(content[2])
            self.Pir=float(content[3])


#Ps, Pi et Pr fixent les probabilites initiales d'etre infecte initialement,
#est-ce utile ? Ou est ce qu'on met tout les I et R a 0 au debut avec tout le monde sain, pas encore malade ?
#Psi = Proba qu'un sain devienne infecte
#Pir = Proba qu'un infecte devienne resistant


print '##### PROJET 3BIM - INSA Lyon - Bosc, Greugny, Jaouen, Kuhlburger #####'
s=simulation("SimulationParameters.txt")
print "AVANT DEBUT DE CONTAMINATION"
worldmap=worldCities('Population.csv')
worldmap.infection(s.Psi,s.Pir,5) #On pourrait apres rentrer une maladie en parametre a la place de Psi et Pri et c'est la maladie meme qui definirait les probabilites Psi et Pri
