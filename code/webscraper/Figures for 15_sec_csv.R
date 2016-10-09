#Sample R code, waiting for all results to be in
#Set working directory
setwd("c:\\users\\Ken\\Desktop")

#create table for 15_sec.csv file
table1 <- read.table("15_sec.csv", header=FALSE, sep=",", allowEscapes = FALSE, stringsAsFactors = TRUE)
#assign column names
colnames(table1) <- c("SeverityNum", "SeverityDesc", "VulnType", "VulnDesc", "Path", "NumVulns", "VulnCode", "False", "LawnGreen")

#Graphs
#create histogram to show frequencies of severity
hist(table1$SeverityNum, xlab="Severity Number", main="Histogram of Severity")
#plot CDF of above
plot.ecdf(table1$SeverityNum, verticals=TRUE, main="CDF of Severity", xlab="Severity", ylab="Cumulative Frequency", xlim=c(1,6))
#hist of number of vulnerabilities per line (looks logarithmic but not sure how to scale the plot view). (485 is the highest # of vulns) 
hist(table1$NumVulns, main="Distribution of # of Vulns", xlab="Amount", ylab="Frequency", xlim=c(1,50), breaks=485)
