import numpy as np

class citySIR:

    def __init__(self,S,I,R):
          self.S=S
          self.I=I
          self.R=R
          self.population=[]
          self.population.append(self.S+self.I+self.R)
          print self.population
    
    def infection(self,alpha,gamma,dt,iterations):
        
        print iterations
        
        fich=open("OutputPopulations_CitySIR.txt","w")
        vect = [i for i in np.arange(0,iterations+dt,dt)]

        for j in vect: #Nombre d'iterations d'infection
            #S=self.S
            #I=self.I
            #R=self.R
            #print I
            
            self.S=self.S+dt*(-alpha*self.S*self.I)                 #alpha = taux d'infection
            self.I=self.I+dt*(alpha*self.S*self.I-gamma*self.I)           #gamma = taux de retrait
            self.R=self.R+dt*(gamma*self.I)
            #print self.I
            
            contenu=str(self.S)+'\t'+str(self.I)+'\t'+str(self.R)+'\t'+str(self.R+self.I+self.S)+'\t'+str(j)+'\n';
            fich.writelines(contenu)
            fich.writelines('\n')

        

cityTest=citySIR(11967,10,0)
alpha = 5.4*10**(-5)
tc=7
gamma = float(1.0/tc)
print gamma
dt=0.01
iterations=120
print 'ok'
cityTest.infection(alpha,gamma,dt,iterations)




 #for i in xrange(len(self.population)):
                
                #k=0

                
               # while k<iterations:
               
               
                                   #k+=dt
                #print self.I
                #print self.I+self.R+self.S
                
                #fich.writelines("S \t I \t R \t Total \t Time \n  \n")
                
                #for l in iterations:
