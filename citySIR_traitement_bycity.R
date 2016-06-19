#######################################################################
##### A PARTIR DU PROGRAMME GENERAL PAR VILLE #########################
#######################################################################

city = c('London','Paris','Rome','Berlin')


for (i in 1:length(city)){
  city[i]
  data=read.table(paste("OutputProfilSIR_",city[i],".txt",sep=""),header=T,dec=".",sep="\t")
  S=data[,1]
  I=data[,2]
  R=data[,3]
  pop=data[,4]
  time=data[,5]

  x11()
#  par(mfrow=c(1,2))
<<<<<<< HEAD
  plot(S~time,type='l',main=c('Profil SIR pour',city[i]),xlab='Time',ylab='Population',lwd=1,ylim=c(0,max(max(S),max(I),max(R))))
  lines(I~time,col='red',lwd=1)
  lines(R~time,col='blue',lwd=1)
  legend('topright',legend=c('Sain','Infectés','Résistants'),col=c("black", "red","blue"),lwd=2)
=======
  M = max(max(S),max(I),max(R))
  plot(S~time,type='l',main=c('Profil SIR pour',city[i]),ylim = c(0,M))
  
  lines(I~time,col='red')
  lines(R~time,col='blue')
>>>>>>> origin/master
}