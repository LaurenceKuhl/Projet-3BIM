
#setwd("~/Documents/Projet 3BIM/Projet-3BIM")
rm(list = ls())

t = read.table("OutputPopulations.txt", header  = T, sep = "\t")

##### Obtention de tableaux de noms, S, I, R, Total et Time #####
Name=t[,1]
S=t[,2]
I=t[,3]
R=t[,4]
Total=t[,5]
Time=t[,6]

##### Obtenir les données par ville ##### (Besoin trouver une boucle pour le faire automatiquement pour chaque ville)
London=t[t$Name == 'London',]
Paris=t[t$Name == 'Paris',]

##### Affichage des populations S, I et R avec des types différents pour chaque ville #####
plot(London$Time,London$S,col='red',type='l',xlab='Time',ylab='Population',main='Time evolution of populations')
lines(London$Time,London$I,col='blue')
lines(London$Time,London$R,col='green')
points(Paris$Time,Paris$S,col='red')
points(Paris$Time,Paris$I,col='blue')
points(Paris$Time,Paris$R,col='green')
legend("topright",legend=c('Safe','Infected','Retired'),col=c('red','blue','green'),lty=1)
