# -*- coding: utf-8 -*-
import city

class simulation:
    
    def __init__(self,field):

        ##### Import parameters #####
        with open(field,'r') as f:
            content = f.readlines()
            for i in range(len(content)):
                content[i]=content[i].split("\t")[0]
            self.Psi=content[2]
            self.Pir=content[3]


#Ps, Pi et Pr fixent les probabilités initiales d'être infecté initialement,
#est-ce utile ?
#Psi = Proba qu'un sain devienne infecté
#Pir = Proba qu'un infecté devienne résistant


print '##### PROJET 3BIM - INSA Lyon - Bosc, Greugny, Jaouen, Kuhlburger #####'
simulation("SimulationParameters.txt")
worldmap=city('Population.csv')
print worldmap.infection()
