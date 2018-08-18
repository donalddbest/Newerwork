# Title: prettypictures.R
# Author: Donald DiJacklin


# The purpose of this script is to 
rm(list = ls())
library('dplyr')

# Reads in data
data = read.csv('../Data/probprofitfile.csv', header = FALSE)
mfdata = read.csv('../Data/mffile.csv', header = FALSE)


# Filters data by the given parameter
greedy <- data %>% filter(V10 == .6) %>% mutate(TotalProfit = V1+V2+V3+V4+V5+V6+V7+V8)%>%arrange(TotalProfit)%>%mutate(weight = 1/length(TotalProfit))%>%mutate(probbefore = cumsum(weight))
# arbitrary <- data %>% filter(V9 == 1) %>% mutate(TotalProfit = V1+V2+V3+V4+V5+V6+V7+V8)%>%arrange(TotalProfit)%>%mutate(weight = 1/length(TotalProfit))%>%mutate(probbefore = cumsum(weight))
genes <- data %>% filter(V10 == .7) %>% mutate(TotalProfit = V1+V2+V3+V4+V5+V6+V7+V8+9600)%>%arrange(TotalProfit)%>%mutate(weight = 1/length(TotalProfit))%>%mutate(probbefore = cumsum(weight))


# Makes a plot of the ecdfs of the filtered data.
png('../Figures/probECDF.png')
plot(ecdf(genes$TotalProfit),verticals=TRUE, do.points=FALSE, col = 'blue',xlab = 'Total Profit',ylab = 'Empirical Cumulative Density', main = 'Comparing ECDFs', xlim = c(90000,250000))
lines(ecdf(greedy$TotalProfit),verticals=FALSE, do.points=FALSE, col = 'darkred',lwd = 3)
legend(100000,1,c('Probability .7','Probability .6'),col = c('blue','darkred'),lty = c(1,2), lwd = c(1,3))
dev.off()

# Tests for differences in the ECDFs
test<- ks.test(greedy$TotalProfit,genes$TotalProfit)
test
# mu<-mean(greedy$TotalProfit)
# xbar<-mean(genes$TotalProfit)
# sqrt(200)*(xbar-mu)/sd(genes$TotalProfit)
# names(mfdata)<-c('Males','Females','Numbreed')
# vir<- mfdata %>% filter(Numbreed == 6)
# notvir<- mfdata %>% filter(Numbreed == 5)
# mean(vir$Males)
# mean(vir$Females)

# mean(notvir$Males)
# mean(notvir$Females)

# Tests for differences in the means
t.test(genes$TotalProfit,greedy$TotalProfit)

# Tests for differences in the variances
var.test(genes$TotalProfit,greedy$TotalProfit,alternative = 'less')
