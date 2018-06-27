# Title: prettypictures.R
# Author: Donald DiJacklin


# The purpose of this script is to 
rm(list = ls())
library('dplyr')

data = read.csv('profitfile.csv', header = FALSE)

optimum <- data %>% filter(V6 == 0)
arbitrary <- data %>% filter(V6 == 1)

optimsixty <- optimum %>% filter(V7 == .6)
optimseventy <- optimum %>% filter(V7 == .7)

avesix<- c(mean(optimsixty$V1), mean(optimsixty$V2), mean(optimsixty$V3), mean(optimsixty$V4), mean(optimsixty$V5))
avesev<- c(mean(optimseventy$V1), mean(optimseventy$V2), mean(optimseventy$V3), mean(optimseventy$V4), mean(optimseventy$V5))

# Create boxplot
pdf('prelimcompstat.pdf')
plot(c(1,2,3,4,5), avesev, type = 'l', col = 'green', xlab = 'Year', ylab = 'Profit')
lines(c(1,2,3,4,5), avesix, col = 'red')
legend(3.5, 1000, c('Probability of clutch .7','Probability of clutch .6'), col = c('green', 'red'))
dev.off()
