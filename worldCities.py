# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import csv
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#import simulation


class worldCities:
    
    
    #####################################################################################
    ################# Definition of all the cities and their parameters #################
    ##################################################################################### 
    def __init__(self,fieldPop,fieldFly,nbrCriteres,PvoyageS,PvoyageI,PvoyageR):
        
        
	#####Recuperation des donnees des villes #####
        with open(fieldPop,'rb') as file: #Lecture du fichier
            contents = csv.reader(file)
            pop = list()
            for row in contents:
                pop.append(row)        
                  
            
            for i in xrange(0,3): #Supprimer les 4 premieres et 3 dernieres lignes
                pop.pop(0)
                pop.pop(-1)
            pop.pop(0)
            
            for i in xrange(len(pop)): #Separation du tableau pop
                #print nbrCriteres
                for j in xrange(1,nbrCriteres-1):
                    pop[i].append(float(pop[i][0].split(";")[j]))
                pop[i].append(pop[i][0].split(";")[nbrCriteres-1])
                pop[i][0]=pop[i][0].split(";")[0]
                #Faut il fermer le fichier

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
#            self.m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c') ###Creation de la carte
            self.pVoyS = []
            self.pVoyI = []
            self.pVoyR = []
             
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
                self.pVoyS.append([pop[i][9],1])
                self.pVoyI.append([pop[i][9],1])
                self.pVoyR.append([pop[i][9],1])
                #print "Ville a t0 : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]
                self.nbrCities=len(self.name)
	
	
	
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





        ################################################################################
        ###########                Infection initiale des individus           ##########
        ################################################################################
        ind=self.convNameIndice('London')
                
        self.I[ind]=10              #Infecte 10 personnes dans la ville 0
        self.S[ind]=self.S[0]-10

        # self.I[1]=10              #Infecte 10 personnes dans la ville 0
        # self.S[1]=self.S[1]-10
        # self.I[2]=10              #Infecte 10 personnes dans la ville 0
        # self.S[2]=self.S[2]-10
        # self.I[3]=10              #Infecte 10 personnes dans la ville 0
        # self.S[3]=self.S[3]-10
        # self.I[4]=10              #Infecte 10 personnes dans la ville 0
        # self.S[4]=self.S[4]-10

        ##### S'assurer du nombre de personnes constant en l"absence de naissances #####
        worldPopulation=0
        for i in self.indice:
            worldPopulation+=self.R[i]+self.I[i]+self.S[i]
        print "Population initiale ",worldPopulation






    #####################################################################################
    ##### Classe d'infection des populations au sein d'une meme ville, sans echange #####
    #####################################################################################
    def infection(self,alpha,tc,dt,iterations,StudiedCities,bigIter):
                
        gamma=1.0/tc

        f = open("test.txt",'w')
        
        for i in xrange(len(self.population)):
            f.writelines(str(i)+"\n")
            vect = [l for l in np.arange(0,iterations+dt,dt)]
            for j in vect: #Nombre d'iterations d'infection

                self.S[i]=self.S[i]+dt*(-alpha*self.S[i]*self.I[i])                        #alpha = taux d'infection
                self.I[i]=self.I[i]+dt*(alpha*self.S[i]*self.I[i]-gamma*self.I[i])          #gamma = taux de retrait
                self.R[i]=self.R[i]+dt*(gamma*self.I[i])




                if i in StudiedCities :
                    if j%1 == 0:
                        self.profilSIR(i,fich,bigIter*iterations+j/1)
                
            #print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]
        
        ##### S'assurer du nombre de personnes constant en absence de naissances #####
	#worldPopulation=0
        #for i in self.indice:
        #    worldPopulation+=self.R[i]+self.I[i]+self.S[i]
        #print "After infection",worldPopulation

    """
    ANCIEN MODELE SIR
	       self.R[i]=self.R[i]+(Pir*self.I[i])//1                         #Avec la probabilite Pir de passer du stade I a R
	       self.I[i]=self.I[i]-(Pir*self.I[i])//1+(Psi*self.S[i])//1     #Avec la probabilite Pir de passer du stade I a R soustraite et Psi celle de passer de S a I ajoutee 
	       self.S[i]=self.S[i]-(Psi*self.S[i])//1                         #Avec la probabilite Psi de passer stade S a I
	       
	       #print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]
	
    """

	

	
	
    #####################################################################################
    ########### Compter la population totale de la mapemonde ############################
    #####################################################################################    

    ##### S'assurer du nombre de personnes constant en absence de naissances #####
    #worldPopulation=0
    #for i in self.indice:
    #    worldPopulation+=self.R[i]+self.I[i]+self.S[i]
    #print "After infection",worldPopulation



    #####################################################################################
    ########### Afficher le profil SIR d'une ville ######################################
    #####################################################################################    


    def profilSIR(self,indiceVille,fich,iternumber):
        fich=open(str("OutputProfilSIR_"+str(self.name[indiceVille])+".txt"),"a")
        contenu=str(self.S[indiceVille])+'\t'+str(self.I[indiceVille])+'\t'+str(self.R[indiceVille])+'\t'+str(self.R[indiceVille]+self.I[indiceVille]+self.S[indiceVille])+'\t'+str(iternumber)+'\n';
        fich.writelines(contenu)
        fich.writelines('\n')



    """
    #####################################################################################
    ############### Classe d'affichage de la mapemonde ##################################
    #####################################################################################    
    def maps(self,DENSITY):
		# Draw coastlines, and the edges of the map.
		self.m.drawcoastlines()
		self.m.drawmapboundary()
		self.m.bluemarble()
		# Convert latitude and longitude to x and y coordinates
		x, y = self.m(list(self.longitude), list(self.latitude))
		# Use matplotlib to draw the points onto the map.
		for i in self.indice:
			if self.density_infected[i]>=DENSITY:
				x,y=self.m(self.longitude[i],self.latitude[i])
				self.m.plot(x,y,marker='o',color='red')
			else:
				x,y=self.m(self.longitude[i],self.latitude[i])
				self.m.plot(x,y,marker='o',color='green')
		#m.drawcoastlines() différentes options cool si vous voulez les rajouter!
		#m.drawstates()
		#m.drawcountries()
		plt.show()
    
    def drawflights(self,densite_vol):
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
				if self.fly[i][j] > densite_vol:
					m.drawgreatcircle(self.longitude[i],self.latitude[i],self.longitude[j],self.latitude[j],linewidth=2,color='b') 
			
		plt.show()
    """    
    
    
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
        
        ##### Population mouvements #####        
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
                    self.R[i]+=(sauvegardeR[j]*PvoyageR*self.fly[i][j])
                    self.I[i]+=(sauvegardeI[j]*PvoyageI*self.fly[i][j])
                    self.S[i]+=(sauvegardeS[j]*PvoyageS*self.fly[i][j])
                                        
                    #Départ de la ville i
                    self.R[i]-=(sauvegardeR[i]*PvoyageR*self.fly[i][j])
                    self.I[i]-=(sauvegardeI[i]*PvoyageI*self.fly[i][j])
                    self.S[i]-=(sauvegardeS[i]*PvoyageS*self.fly[i][j])
                    
                    #Arrivées dans la ville j
                    self.R[j]+=(sauvegardeR[i]*PvoyageR*self.fly[i][j])
                    self.I[j]+=(sauvegardeI[i]*PvoyageI*self.fly[i][j])
                    self.S[j]+=(sauvegardeS[i]*PvoyageS*self.fly[i][j])
                    
                    #Départ de la ville j
                    self.R[j]-=(sauvegardeR[j]*PvoyageR*self.fly[i][j])
                    self.I[j]-=(sauvegardeI[j]*PvoyageI*self.fly[i][j])
                    self.S[j]-=(sauvegardeS[j]*PvoyageS*self.fly[i][j])

            #print "Ville : ",self.name[i]," S=",self.S[i]," I=",self.I[i]," R=",self.R[i]

    	##### S'assurer du nombre de personnes constant en absence de naissances #####
        #worldPop=0
        #for i in self.indice:
        #    worldPop+=self.R[i]+self.I[i]+self.S[i]
        #print "After mouvement ",worldPop
        #print "Diff=",worldPopulation-worldPop #Des écarts de moins de 1000 personnes à cause des arrondis selon moi



    #####################################################################################
    ############### Classe de mouvement des populations entre villes ####################
    ##################     en fonction de la concentration         ######################
    #####################################################################################

    #methode de transport avec populations des villes constantes et modification des proportions
    #Dans un premier temps j'ai gardé les tableaux S I et R comme au début
    #Ensuite on stockera directement les proportions à l'intérieur
    def transportbis(self):
   
        ##### Safeguard before first move #####
        sauvegardeR=[]
        sauvegardeI=[]
        #sauvegardeS=[]
        #tS_old =[]
        tI_old = []
        tR_old = []

        for i in self.indice:
            sauvegardeR.append(self.R[i])
            sauvegardeI.append(self.I[i])
            #sauvegardeS.append(self.S[i])
            #tS_old.append(float(self.S[i])/self.population[i])
            tI_old.append(float(self.I[i])/self.population[i])
            tR_old.append(float(self.R[i])/self.population[i])

        #cumulTauxS = np.zeros(len(self.population))
        cumulTauxI = np.zeros(len(self.population))
        cumulTauxR = np.zeros(len(self.population))
        #cumulpopS = np.zeros(len(self.population))
        cumulpopI = np.zeros(len(self.population))
        cumulpopR = np.zeros(len(self.population))
        
        #print tI_old
        
        for i in self.indice:
            for j in self.indice :
                #if j>i:
                                    
                    if ((self.pVoyS[i][1]>tI_old[j]) and (self.pVoyI[i][1]>tI_old[j]) and (self.pVoyR[i][1]>tI_old[j])):
                        
                        #Voyage des S
                        #cumulTauxS[i] += tS_old[j]*self.population[j]*self.pVoyS[j][0]*self.fly[i][j]
                        #cumulpopS[i] += self.population[j]*self.pVoyS[j][0]*self.fly[i][j]
                        #Voyage des I
                        cumulTauxI[i] += tI_old[j]*self.population[j]*self.pVoyI[j][0]*self.fly[i][j]
                        cumulpopI[i] += self.population[j]*self.pVoyI[j][0]*self.fly[i][j]
                        #Voyage des R
                        cumulTauxR[i] += tR_old[j]*self.population[j]*self.pVoyR[j][0]*self.fly[i][j] #*100*100
                        cumulpopR[i] += self.population[j]*self.pVoyR[j][0]*self.fly[i][j]
                    
                    #if ((self.pVoyS[j][1]>tI_old[i]) and (self.pVoyI[j][1]>tI_old[i]) and (self.pVoyR[j][1]>tI_old[i])):

                        #cumulTauxS[j] += tS_old[i]*self.population[i]*self.pVoyS[i][0]*self.fly[i][j]
                        #cumulpopS[j] += self.population[i]*self.pVoyS[i][0]*self.fly[i][j]
                        
                        #Voyage des I
                        #cumulTauxI[j] += tI_old[i]*self.population[i]*self.pVoyI[i][0]*self.fly[i][j]
                        #cumulpopI[j] += self.population[i]*self.pVoyI[i][0]*self.fly[i][j]
                        
                        #Voyage des R
                        #cumulTauxR[j] += tR_old[i]*self.population[i]*self.pVoyR[i][0]*self.fly[i][j]
                        #cumulpopR[j] += self.population[i]*self.pVoyR[i][0]*self.fly[i][j]
        
        print cumulTauxR
        print cumulTauxI                
                                                        
        for c in self.indice :
            self.I[c] = (tI_old[c]*self.population[c] + cumulTauxI[c])/(self.population[c]+cumulpopI[c])* self.population[c]
            self.R[c] = (tR_old[c]*self.population[c] + cumulTauxR[c])/(self.population[c]+cumulpopR[c])* self.population[c]

            #on deduit le nouveau nombre de S a partir du nouveau nb de I et de R
            self.S[c] = self.population[c] - (self.I[c] + self.R[c])

            self.density_infected[c] = self.I[c] / float(self.population[c])

            #print "Ville : ",self.name[c]," S=",self.S[c]," I=",self.I[c]," R=",self.R[c], "Densite d'infectes",self.density_infected[c]



    #####################################################################################
    ######################## Classe de mort dans chaque ville ###########################
    #####################################################################################
    def death(self,PdR,PdI,PdS):

        for i in self.indice:
            self.R[i]-=(self.R[i]*PdR)
            self.I[i]-=(self.I[i]*PdI)
            self.S[i]-=(self.S[i]*PdS)
            
            self.density_infected[i]=self.I[i]/self.population[i] 
    
    
    #####################################################################################
    #################### Classe de naissances dans chaque ville #########################
    #####################################################################################           
    def birth(self,PbR,PbI,PbS):

        for i in self.indice:        
            self.R[i]+=(self.R[i]*PbR)  #Est-ce que les R font naitre forcement des R ?
            self.I[i]+=(self.I[i]*PbI) #Est-ce que les I font naitre forcement des I ?
            self.S[i]+=(self.S[i]*PbS)
            
            self.density_infected[i]=self.I[i]/self.population[i]
    
    
    
    #####################################################################################
    ######## Classe de fermeture des aéroports selon une liste d'indices reçue ##########
    #####################################################################################
    def closeAirports(self,closedAirportsIndex):
        
        for i in range(len(closedAirportsIndex)):
            
            closedAirportsIndex[i][0]=self.convNameIndice(closedAirportsIndex[i][0])

            # Changer la probabilite de voyager selon le niveau d'urgence
            if closedAirportsIndex[i][1]==1:

                if self.pVoyI[closedAirportsIndex[i][0]][0]>0.3:
                    self.pVoyI[closedAirportsIndex[i][0]][0] = 0.1
                else :
                    self.pVoyI[closedAirportsIndex[i][0]][0] = self.pVoyI[closedAirportsIndex[i][0]][0] - 0.3
                    
            elif closedAirportsIndex[i][1]==2:
                self.pVoyI[closedAirportsIndex[i][0]][0]=0
                
            elif closedAirportsIndex[i][1]==3:

                self.pVoyS[closedAirportsIndex[i][0]][0]=0
                self.pVoyI[closedAirportsIndex[i][0]][0]=0
                self.pVoyR[closedAirportsIndex[i][0]][0]=0
                
            self.pVoyS[closedAirportsIndex[i][0]][1]=closedAirportsIndex[i][2]            
            self.pVoyI[closedAirportsIndex[i][0]][1]=closedAirportsIndex[i][2]
            self.pVoyR[closedAirportsIndex[i][0]][1]=closedAirportsIndex[i][2]          

    #####################################################################################
    ############## Classe de conversion d'un nom de ville en indice #####################
    #####################################################################################
    def convNameIndice(self,name):
        i=0
        while i<len(self.name):
            if (self.name[i]==name) :
                return i
            i+=1
        print("Error : %s dosen\'t appear in database." % (name))
        return False



################################################################################
#####################    CLASSE SIMULATION    ##################################
################################################################################

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
            self.alpha=float(content[2])
            self.tc=float(content[3])
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
            self.dt=float(content[14])
            self.Tsim=int(content[15])
            self.Tinf=int(content[16])
            
"""
Ps, Pi et Pr fixent les probabilites initiales d'etre infecte initialement,
est-ce utile ? Ou est ce qu'on met tout les I et R a 0 au debut avec tout le monde sain, pas encore malade ?
Psi = Proba qu'un sain devienne infecte
Pir = Proba qu'un infecte devienne resistant
"""








################################################################################
################        LANCEMENT DU PROGRAMME          ########################
################################################################################


print '##### PROJET 3BIM - INSA Lyon - Bosc, Greugny, Jaouen, Kuhlburger #####'
s=simulation("SimulationParameters.txt")
print "AVANT DEBUT DE CONTAMINATION"
worldmap=worldCities('Population.csv','FlyFrequency.csv',s.nombreCriteres,s.PvoyageS,s.PvoyageI,s.PvoyageR)

########################### VILLES ETUDIEES ####################################

StudiedCities=['London','Paris','Singapore','Budapest','Berlin']    #Indices des villes à étudier
for c in range(len(StudiedCities)):
    fich=open(str("OutputProfilSIR_"+str(StudiedCities[c])+".txt"),"w")
    fich.writelines("S\tI\tR\tTotal\tTime\n\n")
    StudiedCities[c] = worldmap.convNameIndice(StudiedCities[c])
    fich.close()

##########################  AEROPORTS FERMES ###################################

#ClosedAirportsIndex est une liste de tuples. Ces tuples sont composes de l'indice
#de l'aeroport a fermer et le niveau d'urgence avec lequel le fermer :
# 1 - Empecher la moitie des infectes de voyager
# 2 - Empecher 9/10e des infectes de voyager
# 3 - Empecher tous les individus S, I et R de voyager

#Imposer un taux maximal d'infectes dans le pays avec lequel on communique

closedAirportsIndex=[['Paris',1,0.1],['Berlin',0,0.8],['Singapore',0,0.8],['London',0,0]]



#########################   LANCEMENT DU PROGRAMME #############################

fold=open("Globaldata.txt","w")
fold.writelines("Population mondiale\t S \t I \t R \t t \n")

#worldmap.density_infected[0]=1.2
#worldmap.maps(0.01)

fich=open("OutputPopulations.txt","w")
fich.writelines("Name\t S \t I \t R \t Total \t Time \n  \n")

#worldmap.closeAirports(closedAirportsIndex)

for i in xrange(s.Tsim): #20 iterations dans lesquelles on a 5 iterations d'infection entre chaque processus de mouvement
    
	print "ITERATION ",i+1

	#worldmap.death(s.PdR,s.PdI,s.PdS)
	#worldmap.birth(s.PbR,s.PbI,s.PbS)

	worldmap.infection(s.alpha,s.tc,s.dt,s.Tinf,StudiedCities,i) #On pourrait apres rentrer une maladie en parametre a la place de Psi et Pri et c'est la maladie meme qui definirait les probabilites Psi et Pri

	worldmap.transportbis() #Mouvement des populations par transport

	worldPopulation=0
	S_=0
	I_=0
	R_=0
	for j in worldmap.indice:
		worldPopulation+=worldmap.R[j]+worldmap.I[j]+worldmap.S[j]
		S_+=worldmap.S[j]
		R_+=worldmap.R[j]
		I_+=worldmap.I[j]
	content=str(worldPopulation)+'\t'+str(S_)+'\t'+str(I_)+'\t'+str(R_)+'\t'+str(i	)+'\n'+'\n'
	fold.writelines(content)
	#print worldPopulation

	for j in worldmap.indice:
	    fich=open("OutputPopulations.txt","a")
	    contenu=str(worldmap.name[j])+'\t'+str(worldmap.S[j])+'\t'+str(worldmap.I[j])+'\t'+str(worldmap.R[j])+'\t'+str(worldmap.R[j]+worldmap.I[j]+worldmap.S[j])+'\t'+str(i)+'\n';
	    fich.writelines(contenu)
	fich.writelines('\n')
	fich.close()

################################################################################