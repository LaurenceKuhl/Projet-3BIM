#######################################################################
##### A PARTIR DU PROGRAMME GENERAL PAR VILLE #########################
#######################################################################

city = c('London','Paris','Singapore','Budapest','Berlin')


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
  plot(S~time,type='l',main=c('Profil SIR pour',city[i]),xlab='Time',ylab='Population',lwd=1,ylim=c(0,max(max(S),max(I),max(R))))
  lines(I~time,col='red',lwd=1)
  lines(R~time,col='blue',lwd=1)
  legend('topright',legend=c('Sain','Infectés','Résistants'),col=c("black", "red","blue"),lwd=2)
}
