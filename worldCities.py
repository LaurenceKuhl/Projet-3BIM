# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#import simulation


class worldCities:
    
    #####################################################################################
    ################# Definition of all the cities and their parameters #################
    ##################################################################################### 
    def __init__(self,fieldPop,fieldFly,nbrCriteres):
        
	#####Recuperation des donnees des villes #####
        with open(fieldPop,'rb') as file: #Lecture du fichier
            contents = csv.reader(file)
            pop = list()
            for row in contents:
                pop.append(row)        
            
            #print pop                    
            
            for i in xrange(0,3): #Supprimer les 4 premieres et 3 dernieres lignes
                pop.pop(0)
                pop.pop(-1)
            pop.pop(0)
            
            for i in xrange(len(pop)): #Separation du tableau pop
                print nbrCriteres
                for j in xrange(1,nbrCriteres-1):
                    pop[i].append(float(pop[i][0].split(";")[j]))
                pop[i].append(pop[i][0].split(";")[nbrCriteres-1])
                pop[i][0]=pop[i][0].split(";")[0]
                #Faut il fermer le fichier
            
            #print pop


	   #Creation de tableaux de noms, indices, populations... dont les lignes correspondent aux differentes villes
            self.name=[]
            self.indice=[]
            self.population=[]
            self.S=[]
            self.I=[]
            self.R=[]
            self.density=[]
            self.area=[]
            self.latitude=[]
            self.longitude=[]
            self.density_infected=[]
            for i in xrange(len(pop)):
                self.name.append(pop[i][0])
                self.indice.append(int(pop[i][1])-1)
                self.population.append(pop[i][3])
                self.S.append(self.population[i])
                self.I.append(0)
                self.R.append(0)
                self.density_infected.append(0)
                self.density.append(pop[i][5])
                self.area.append((self.S[i]+self.I[i]+self.R[i])/self.density[i]) #Peut etre inutile
                self.latitude.append(pop[i][6])
                self.longitude.append(pop[i][7])
                #print "Ville a t0 : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]
                self.nbrCities=len(self.name)
            print self.R
	
	##### Import airplane flies matrix #####
        with open(fieldFly,'rb') as file:
            contents = csv.reader(file)
            self.fly = list()
            for row in contents:
                self.fly.append(row)
            
            for i in xrange(0,4):
                self.fly.pop(0)
            
            for i in xrange(len(self.fly)): #Separation du tableau pop
                for j in xrange(1,self.nbrCities+2):
                    temp=self.fly[i][0].split(";")[j]
                    if (len(temp)!=0):
                        self.fly[i].append(float(temp))
                    else:
                        self.fly[i].append(0) #Surcharge de memoire avec des 0, c'est inutile, reflechir a comment faire autrement
                self.fly[i].pop(0)
                self.fly[i].pop(0)
        #Faut il fermer le fichier


        ##### S'assurer du nombre de personnes constant en l"absence de naissances #####
        worldPopulation=0
        for i in self.indice:
            worldPopulation+=self.R[i]+self.I[i]+self.S[i]
        print "Population initiale ",worldPopulation
        



    #####################################################################################
    ##### Classe d'infection des populations au sein d'une meme ville, sans echange #####
    #####################################################################################
    def infection(self,Psi,Pir,iterations):
	
	for j in xrange(iterations): #Nombre d'iterations d'infection
	   #print "CONTAMINATION NUMBER ",j+1
	   
	   for i in xrange(len(self.population)):
	       self.R[i]=self.R[i]+(Pir*self.I[i])//1                         #Avec la probabilite Pir de passer du stade I a R
	       self.I[i]=self.I[i]-(Pir*self.I[i])//1+(Psi*self.S[i])//1     #Avec la probabilite Pir de passer du stade I a R soustraite et Psi celle de passer de S a I ajoutee 
	       self.S[i]=self.S[i]-(Psi*self.S[i])//1                         #Avec la probabilite Psi de passer stade S a I
	       
	       #print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]
	
	
	##### S'assurer du nombre de personnes constant en absence de naissances #####
        #worldPopulation=0
        #for i in self.indice:
        #    worldPopulation+=self.R[i]+self.I[i]+self.S[i]
        #print "After infection",worldPopulation


    #####################################################################################
    ############### Classe d'affichage de la mapemonde ##################################
    #####################################################################################    
    def map(self):
	
		# Create a map on which to draw.  We're using a mercator projection, and showing the whole world.
		m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
		# Draw coastlines, and the edges of the map.
		m.drawcoastlines()
		m.drawmapboundary()
		# Convert latitude and longitude to x and y coordinates
		x, y = m(list(self.longitude), list(self.latitude))
		# Use matplotlib to draw the points onto the map.
		m.scatter(x,y,1,marker='O',color='green')
		#m.drawcoastlines() différentes options cool si vous voulez les rajouter!
		#m.drawstates()
		#m.drawcountries()
		plt.show()
    
    def drawflights(self,INDICE):
		# Create a map on which to draw.  We're using a mercator projection, and showing the whole world.
		m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
		# Draw coastlines, and the edges of the map.
		m.drawcoastlines()
		m.drawmapboundary()
		# Convert latitude and longitude to x and y coordinates
		x, y = m(list(self.longitude), list(self.latitude))
		# Use matplotlib to draw the points onto the map.
		m.scatter(x,y,10,marker='o',color='green')
		m.drawcoastlines() #différentes options cool si vous voulez les rajouter!
		m.drawstates()
		m.drawcountries()
		for i in self.indice:
			for j in self.indice:
				if self.fly[i][j] > INDICE:
					m.drawgreatcircle(self.longitude[i],self.latitude[i],self.longitude[j],self.latitude[j],linewidth=2,color='b') 
			
		plt.show()
    
    #####################################################################################
    ############### Classe de mouvement des populations entre villes ####################
    #####################################################################################
    def transport(self,PvoyageS,PvoyageI,PvoyageR):      
                                
        ##### Safeguard before first move #####
        sauvegardeR=[]
        sauvegardeI=[]
        sauvegardeS=[]

        for i in self.indice:
            sauvegardeR.append(self.R[i])
            sauvegardeI.append(self.I[i])
            sauvegardeS.append(self.S[i])
        #print "En 5=",sauvegardeS[5]
        
        ##### Population mouvements #####
        
        #worldPopulation=0
        #for i in self.indice:
        #    worldPopulation+=self.R[i]+self.I[i]+self.S[i]
        #print "Before move",worldPopulation
        
        
        """
        Chaque etat S, I et R a sa propre probabilite de voyage pour l'instant.
        Ainsi, dans chaque ville, on envoie une proportion PvoyageR de la population
        R vers une autre ville. De meme pour chaque etat.
        La sauvegarde sert a calculer la part de la population qui voyage entre l'instant
        t et t+1. Pour cela, nous devons stocker les 2 instants pour que les populations
        ne bougent pas entre les calculs.
        Self.fly[i][j] regroupe la probabilite de decoler de la ville i pour se rendre
        vers la ville j.
        Pour chaque ville i, on fait arriver des gens de toutes les villes j. On aura
        aussi forcement un depart avec une probabilite PvoyageR de la population R de
        la ville. D'ou le dernier calcul.
        """
        for i in self.indice:
            for j in self.indice:
                if j>i: #Car matrice diagonale, en considérant des allers et retours équivalents d'une ville à l'autre
                    
                    #Arrivées dans la ville i
                    self.R[i]+=(sauvegardeR[j]*PvoyageR*self.fly[i][j])//1
                    self.I[i]+=(sauvegardeI[j]*PvoyageI*self.fly[i][j])//1
                    self.S[i]+=(sauvegardeS[j]*PvoyageS*self.fly[i][j])//1
                                        
                    #Départ de la ville i
                    self.R[i]-=(sauvegardeR[i]*PvoyageR*self.fly[i][j])//1
                    self.I[i]-=(sauvegardeI[i]*PvoyageI*self.fly[i][j])//1
                    self.S[i]-=(sauvegardeS[i]*PvoyageS*self.fly[i][j])//1
                    
                    #Arrivées dans la ville j
                    self.R[j]+=(sauvegardeR[i]*PvoyageR*self.fly[i][j])//1
                    self.I[j]+=(sauvegardeI[i]*PvoyageI*self.fly[i][j])//1
                    self.S[j]+=(sauvegardeS[i]*PvoyageS*self.fly[i][j])//1
                    
                    #Départ de la ville j
                    self.R[j]-=(sauvegardeR[j]*PvoyageR*self.fly[i][j])//1
                    self.I[j]-=(sauvegardeI[j]*PvoyageI*self.fly[i][j])//1
                    self.S[j]-=(sauvegardeS[j]*PvoyageS*self.fly[i][j])//1

            print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i],

    	##### S'assurer du nombre de personnes constant en absence de naissances #####
        #worldPop=0
        #for i in self.indice:
        #    worldPop+=self.R[i]+self.I[i]+self.S[i]
        #print "After mouvement ",worldPop
        #print "Diff=",worldPopulation-worldPop #Des écarts de moins de 1000 personnes à cause des arrondis selon moi


    #methode de transport avec populations des villes constantes et modification des proportions
    #Dans un premier temps j'ai gardé les tableaux S I et R comme au début
    #Ensuite on stockera directement les proportions à l'intérieur
    def transportbis(self,PvoyageS,PvoyageI,PvoyageR):
         ##### Safeguard before first move #####
        sauvegardeR=[]
        sauvegardeI=[]
        sauvegardeS=[]

        for i in self.indice:
            sauvegardeR.append(self.R[i])
            sauvegardeI.append(self.I[i])
            sauvegardeS.append(self.S[i])

        for i in self.indice:
            for j in self.indice:
                if j>i:

                    #Calcul des proportions d'individus S,I et R dans les deux villes
                    tSi_old = sauvegardeS[i]/self.population[i]
                    tSj_old = sauvegardeS[j]/self.population[j]

                    tIi_old = sauvegardeI[i]/self.population[i]
                    tIj_old = sauvegardeI[j]/self.population[j]

                    tRi_old = sauvegardeR[i]/self.population[i]
                    tRj_old = sauvegardeR[j]/self.population[j]

                    #Voyage des S
                    tSi_new =(tSi_old*self.population[i]+tSj_old*self.population[j]*PvoyageS*self.fly[i][j])/(self.population[i]+self.population[j]*PvoyageS*self.fly[i][j])
                    tSj_new =(tSj_old*self.population[j]+tSi_old*self.population[i]*PvoyageS*self.fly[i][j])/(self.population[j]+self.population[i]*PvoyageS*self.fly[i][j])

                    #Voyage des I
                    tIi_new =(tIi_old*self.population[i]+tIj_old*self.population[j]*PvoyageI*self.fly[i][j])/(self.population[i]+self.population[j]*PvoyageI*self.fly[i][j])
                    tIj_new =(tIj_old*self.population[j]+tIi_old*self.population[i]*PvoyageI*self.fly[i][j])/(self.population[j]+self.population[i]*PvoyageI*self.fly[i][j])

                    #Voyage des R
                    tRi_new =(tRi_old*self.population[i]+tRj_old*self.population[j]*PvoyageR*self.fly[i][j])/(self.population[i]+self.population[j]*PvoyageR*self.fly[i][j])
                    tRj_new =(tRj_old*self.population[j]+tRi_old*self.population[i]*PvoyageR*self.fly[i][j])/(self.population[j]+self.population[i]*PvoyageR*self.fly[i][j])

                    #Changement des populations S I et R des deux villes
                    self.S[i] = (tSi_new * self.population[i])//1
                    self.S[j] = (tSj_new * self.population[j])//1
                    self.I[i] = (tIi_new * self.population[i])//1
                    self.I[j] = (tIj_new * self.population[j])//1
                    self.R[i] = (tRi_new * self.population[i])//1
                    self.R[j] = (tRj_new * self.population[j])//1
                    
                    self.density_infected[i]=self.I[i]/self.population[i]  #Mis à jour de la densite d'infectes
                    self.density_infected[j]=self.I[j]/self.population[j]
                   

            print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i], "Densité d'infectés",self.density_infected[i]



    #####################################################################################
    ######################## Classe de mort dans chaque ville ###########################
    #####################################################################################
    def death(self,PdR,PdI,PdS):

        for i in self.indice:
            self.R[i]-=(self.R[i]*PdR)//1
            self.I[i]-=(self.I[i]*PdI)//1
            self.S[i]-=(self.S[i]*PdS)//1
            
            self.density_infected[i]=self.I[i]/self.population[i] 
    
    
    #####################################################################################
    #################### Classe de naissances dans chaque ville #########################
    #####################################################################################
    
            
    def birth(self,PbR,PbI,PbS):

        for i in self.indice:        
            self.R[i]+=(self.R[i]*PbR)//1 #Est-ce que les R font naitre forcement des R ?
            self.I[i]+=(self.I[i]*PbI)//1 #Est-ce que les I font naitre forcement des I ?
            self.S[i]+=(self.S[i]*PbS)//1
            
            self.density_infected[i]=self.I[i]/self.population[i] 



######################################################################################
"""
J'aurais bien aime que la suite soit sur le fichier simulation.py, faire plusieurs 
classes pour lancer le programme mais je n'ai pas reussi a faire le lien entre les
classes car une city doit etre creee dans simulation tout en utilisant les variables
de simulation...
"""

class simulation:
    
    def __init__(self,field):

        ##### Import parameters #####
        with open(field,'r') as f:
            content = f.readlines()
            #print content
            #print len(content)
            for i in range(len(content)):
                content[i]=content[i].split("\t")[0]
            self.Psi=float(content[2])
            self.Pir=float(content[3])
            self.PvoyageS=float(content[4])
            self.PvoyageI=float(content[5])
            self.PvoyageR=float(content[6])
            self.PdS=float(content[7])
            self.PdI=float(content[8])
            self.PdR=float(content[9])
            self.PbS=float(content[10])
            self.PbI=float(content[11])
            self.PbR=float(content[12])
            self.nombreCriteres=int(content[13])
            
"""
Ps, Pi et Pr fixent les probabilites initiales d'etre infecte initialement,
est-ce utile ? Ou est ce qu'on met tout les I et R a 0 au debut avec tout le monde sain, pas encore malade ?
Psi = Proba qu'un sain devienne infecte
Pir = Proba qu'un infecte devienne resistant
"""


print '##### PROJET 3BIM - INSA Lyon - Bosc, Greugny, Jaouen, Kuhlburger #####'
s=simulation("SimulationParameters.txt")
print "AVANT DEBUT DE CONTAMINATION"
worldmap=worldCities('Population.csv','FlyFrequency.csv',s.nombreCriteres)

fich=open("OutputPopulations.txt","w")
fich.writelines("Name\t S \t I \t R \t Total \t Time \n  \n")
worldmap.drawflights(0.2)


for i in xrange(20): #20 iterations dans lesquelles on a 5 iterations d'infection entre chaque processus de mouvement

	print "ITERATION ",i
	worldmap.death(s.PdR,s.PdI,s.PdS)
	worldmap.birth(s.PbR,s.PbI,s.PbS)
	worldmap.infection(s.Psi,s.Pir,5) #On pourrait apres rentrer une maladie en parametre a la place de Psi et Pri et c'est la maladie meme qui definirait les probabilites Psi et Pri
	worldmap.transportbis(s.PvoyageS,s.PvoyageI,s.PvoyageR) #Mouvement des populations par transport
	
	for j in worldmap.indice:
		contenu=str(worldmap.name[j])+'\t'+str(worldmap.S[j])+'\t'+str(worldmap.I[j])+'\t'+str(worldmap.R[j])+'\t'+str(worldmap.R[j]+worldmap.I[j]+worldmap.S[j])+'\t'+str(i)+'\n';
		fich.writelines(contenu)
	fich.writelines('\n')
    
######################################################################################    

        
    
"""	Extrait du SIR fait en TP en debut d'annee			
    def run (self):
		for t in range(self.limiteTime):
			self.move()
			self.reproduce()
			self.rayon=math.sqrt(self.infectedSurface()/math.pi)
			print self.space
			print "Rayon d'infection=%f"%self.rayon
		self.export(self.fichier)
"""
#Crée une densité d'infectés pour pouvoir représenter les villes où y'a trop d'infectés en rouge?
