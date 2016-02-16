X11()

csv <- read.csv(file="libs_stats.csv",head=TRUE,sep=",")
csv[,4] <- NULL

summary(csv)

jpeg(filename="lib_stats_dist.jpg")
# Filled Density Plot
d <- density(csv$Percent.of.Libs.Used)
plot(d, 
	main="Density of Authors Versus Percent of Types Modified or Added", 
	xlab='Percent of Types Modified or Added by Author', 
	ylab='Density of Authors')
polygon(d, border="blue")
dev.off()

Counts <- c()
Threshold50 <- c()
Threshold80 <- c()
for (i in csv$Project){
    Counts <- c(Counts, sum(csv$Project == i))
    Threshold50 <- c(Threshold50, sum(csv[which(csv$Project == i), 3] > 50.0))
    Threshold80 <- c(Threshold80, sum(csv[which(csv$Project == i), 3] > 80.0))
}

csv[, "Authors.Per.Project"] <- Counts
csv[, "Threshold50"] <- Threshold50
csv[, "Threshold80"] <- Threshold80

dd <- csv[!duplicated( csv[ , 1 ] ),]
summary(dd$Authors.Per.Project)
summary(dd$Threshold50)
summary(dd$Threshold80)

jpeg(filename="lib_stats_Threshold50_dist.jpg")
# Filled Density Plot
d <- density(dd$Threshold50, adjust=2, n=8)
plot(d,
	main="Number of Authors per Project that Modified or Added\n over 50% of Types Used in Project", 
	xlab='Number of Authors', 
	ylab='Density of Projects')
polygon(d, border="blue")
axis(side=1, at=c(0, 1, 2, 3, 4, 5, 6, 7, 8))
dev.off()

jpeg(filename="lib_stats_Threshold80_dist.jpg")
# Filled Density Plot
d <- density(dd$Threshold80, adjust=2, n=6)
plot(d,
	main="Number of Authors per Project that Modified or Added\n over 80% of Types Used in Project", 
	xlab='Number of Authors', 
	ylab='Density of Projects')
polygon(d, border="blue")
axis(side=1, at=c(0, 1, 2, 3, 4, 5, 6))
dev.off()

##Go through each row and determine if a value is zero
row_sub <- apply(csv, 1, function(row) row[3] > 0.001 )

##Subset as usual
no_zero_csv <- csv[row_sub,]

summary(no_zero_csv)