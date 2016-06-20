#######################################################################
##### A PARTIR DU PROGRAMME SIR ISOLE #################################
#######################################################################

data=read.table("OutputPopulations_CitySIR.txt",header=F,dec=".",sep="\t")
S=data[,1]
I=data[,2]
R=data[,3]
pop=data[,4]
time=data[,5]

par(mfrow=c(1,2))
plot(S~time,type='l')
plot(I~time,col='red')
lines(R~time,col='blue')