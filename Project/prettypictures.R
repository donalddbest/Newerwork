# Title: prettypictures.R
# Author: Donald DiJacklin


# The purpose of this script is to 
rm(list = ls())
library('dplyr')

data = read.csv('costprofitfile.csv', header = FALSE)
length(data[,1])
greedy <- data %>% filter(V10 == 80) %>% mutate(TotalProfit = V1+V2+V3+V4+V5+V6+V7+V8)%>%arrange(TotalProfit)%>%mutate(weight = 1/length(TotalProfit))%>%mutate(probbefore = cumsum(weight))
arbitrary <- data %>% filter(V9 == 1) %>% mutate(TotalProfit = V1+V2+V3+V4+V5+V6+V7+V8)%>%arrange(TotalProfit)%>%mutate(weight = 1/length(TotalProfit))%>%mutate(probbefore = cumsum(weight))
genes <- data %>% filter(V10 == 90) %>% mutate(TotalProfit = V1+V2+V3+V4+V5+V6+V7+V8)%>%arrange(TotalProfit)%>%mutate(weight = 1/length(TotalProfit))%>%mutate(probbefore = cumsum(weight))
avegreedy <-c()
avegenes<-c()
for (j in 1:(length(data)-2)) {
	avegreedy<-c(avegreedy,mean(greedy[,j], na.rm = TRUE))
	avegenes<-c(avegenes,mean(genes[,j], na.rm = TRUE))
}

avegreedy
avegenes
pdf('RevisedComparisonPlot2.pdf')
plot(1:(length(data)-2),avegenes,type = 'l', col = 'black', xlab = 'Year',ylab = 'Profit')
lines(1:(length(data)-2),avegreedy, col = 'darkred')
legend(2,25100,c('Max Genes','Greedy'),col = c('black','darkred'),lty = 1)
dev.off()
sum(avegreedy)
# sum(avearb)
sum(avegenes)
png('costECDF.png')
plot(ecdf(genes$TotalProfit),verticals=TRUE, do.points=FALSE, col = 'blue',xlab = 'Total Profit',ylab = 'Empirical Cumulative Density', main = 'Comparing ECDFs of the Decision Rules')
lines(ecdf(greedy$TotalProfit),verticals=FALSE, do.points=FALSE, col = 'darkred',lwd = 3)
legend(90000,1,c('Inseminate 6','Inseminate 5'),col = c('blue','darkred'),lty = c(1,2), lwd = c(1,3))
dev.off()

test<- ks.test(greedy$TotalProfit,genes$TotalProfit)
test
mean(greedy$TotalProfit)
mean(genes$TotalProfit)
# optimsixty <- optimum %>% filter(V7 == .6)
# optimseventy <- optimum %>% filter(V7 == .7)

# avesix<- c(mean(optimsixty$V1), mean(optimsixty$V2), mean(optimsixty$V3), mean(optimsixty$V4), mean(optimsixty$V5))
# avesev<- c(mean(optimseventy$V1), mean(optimseventy$V2), mean(optimseventy$V3), mean(optimseventy$V4), mean(optimseventy$V5))

# # Create boxplot
# pdf('prelimcompstat.pdf')
# plot(c(1,2,3,4,5), avesev, type = 'l', col = 'green', xlab = 'Year', ylab = 'Profit')
# lines(c(1,2,3,4,5), avesix, col = 'red')
# legend(3.5, 1000, c('Probability of clutch .7','Probability of clutch .6'), col = c('green', 'red'))
# dev.off()
