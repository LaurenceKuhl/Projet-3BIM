data=read.table("Globaldata.txt",sep="\t",head=TRUE)
time=data$t
pop=data$Population.mondiale
S=data$S
I=data$I
R=data$R



par(mfrow=c(1,3))
plot(time,R,type='l')
title(main="R en fonction du temps")
plot(time,S,type='l')
title(main="S en fonction du temps")
plot(time,I,type='l')
title(main="I en fonction du temps")
