"""This script does the modeling of prices."""
library('dplyr')
library('quantreg')

# Reads in the data
data <- read.csv('../Data/outfile.csv')

# Finds how many genes a snake has.
NumGenes <- c()
for( i in 1:(length(data[,1]))){
	NumGenes<- c(NumGenes, sum(data[i,1:73]))
}
newdata <- cbind(data,NumGenes)

# Finds which genes are represented in less than 10 snakes.
sumvec <- c()
for(i in 1:length(newdata)){
	sumvec <- c(sumvec,sum(newdata[,i]))
}
indlessthree<-which(sumvec<10)
rowinds<-c()
for (i in 1:length(newdata[,1])) {
	for(j in 1:length(indlessthree)){
		if(newdata[i,indlessthree[j]] == 1){
			rowinds<- c(rowinds,i)
			break()
		}
	}
}

newdata<-newdata[-rowinds,]
sumvec <- c()
for(i in 1:length(newdata)){
	sumvec <- c(sumvec,sum(newdata[,i]))
}
indzero<-which(sumvec==0)
newdata<-newdata[,-indzero]
sumvec <- c()
for(i in 1:length(newdata)){
	sumvec <- c(sumvec,sum(newdata[,i]))
}
males<-newdata[which(newdata$Sex == 1),]
females<-newdata[which(newdata$Sex == 0),]

# Models the prices.
model<-lm(formula = log(Price)~.-NumGenes,data = newdata)
coeffs <- summary(model)$coefficients[,1]
newcoeffs <- coeffs + coeffs[1]
newcoeffs <- newcoeffs[-c(1,length(newcoeffs))]
Vars<- ((summary(model)$coefficients[,2])^2)/2
newvars<-Vars+Vars[1]
newvars<-newvars[-c(1,length(newvars))]
prices<-exp(newcoeffs-newvars)-exp(coeffs[1]-Vars[1])
prices<-prices[-8]
genes<-names(prices)
df<-cbind(genes,as.numeric(prices))

# Outputs the results.
write.csv(df,'../Data/newprices.csv',row.names = FALSE)