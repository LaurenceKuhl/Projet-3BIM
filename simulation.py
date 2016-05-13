# -*- coding: utf-8 -*-
import city

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
#est-ce utile ?
#Psi = Proba qu'un sain devienne infecte
#Pir = Proba qu'un infecté devienne resistant


print '##### PROJET 3BIM - INSA Lyon - Bosc, Greugny, Jaouen, Kuhlburger #####'
simulation("SimulationParameters.txt")
worldmap=city('Population.csv')
worldmap.infection()
