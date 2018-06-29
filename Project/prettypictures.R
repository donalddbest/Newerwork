# Title: prettypictures.R
# Author: Donald DiJacklin


# The purpose of this script is to 
rm(list = ls())
library('dplyr')

data = read.csv('newprofitfile.csv', header = FALSE)
length(data[,1])
greedy <- data %>% filter(V6 == 0)
arbitrary <- data %>% filter(V6 == 1)
genes <- data %>% filter(V6 == 2)
avegreedy <- c(mean(greedy[,1]),mean(greedy[,2]),mean(greedy[,3]),mean(greedy[,4]),mean(greedy[,5]))
avearb <- c(mean(arbitrary[,1]),mean(arbitrary[,2]),mean(arbitrary[,3]),mean(arbitrary[,4]),mean(arbitrary[,5]))
avegenes <- c(mean(genes[,1]),mean(genes[,2]),mean(genes[,3]),mean(genes[,4]),mean(genes[,5]))
pdf('RevisedComparisonPlot.pdf')
plot(c(1,2,3,4,5),avearb,type = 'l', col = 'purple', xlab = 'Year',ylab = 'Profit')
lines(c(1,2,3,4,5),avegenes, col = 'blue')
lines(c(1,2,3,4,5),avegreedy, col = 'green')
legend(2,25100,c("Arbitrary",'Max Genes','Greedy'),col = c('purple','blue','green'),lty = 1)
dev.off()
sum(avegreedy)
sum(avearb)
sum(avegenes)

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
