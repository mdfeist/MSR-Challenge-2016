X11()

csv <- read.csv(file="libs_stats.csv",head=TRUE,sep=",")
csv[,5] <- NULL

summary(csv)

jpeg(filename="lib_stats_dist.jpg", width = 4, height = 4, units = 'in', res = 600)
# Filled Density Plot
d <- density(csv$Percent.of.Libs.Used)
plot(d, 
	main="Density of Authors Versus Percent\nof Types Modified or Added", 
	xlab='Percent of Types Modified or Added by Author', 
	ylab='Density of Authors', cex.main=0.75, cex.lab=0.75)
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

jpeg(filename="lib_stats_Threshold50_dist.jpg", width = 4, height = 4, units = 'in', res = 600)
# Filled Density Plot
d <- density(dd$Threshold50, adjust=2, n=8)
plot(d,
	main="Number of Authors per Project that Modified or Added\n over 50% of Types Used in Project", 
	xlab='Number of Authors', 
	ylab='Density of Projects', cex.main=0.75, cex.lab=0.75)
polygon(d, border="blue")
axis(side=1, at=c(0, 1, 2, 3, 4, 5, 6, 7, 8))
dev.off()

jpeg(filename="lib_stats_Threshold80_dist.jpg", width = 4, height = 4, units = 'in', res = 600)
# Filled Density Plot
d <- density(dd$Threshold80, adjust=2, n=6)
plot(d,
	main="Number of Authors per Project that Modified or Added\n over 80% of Types Used in Project", 
	xlab='Number of Authors', 
	ylab='Density of Projects', cex.main=0.75, cex.lab=0.75)
polygon(d, border="blue")
axis(side=1, at=c(0, 1, 2, 3, 4, 5, 6))
dev.off()

jpeg(filename="lib_stats_number_of_libraries_dist.jpg", width = 4, height = 4, units = 'in', res = 600)
# Filled Density Plot
breaks <- c(0,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000)
H <- hist(dd$Number.of.Libraries[dd$Number.of.Libraries < 5000], breaks=256, plot=F)

plot(H$mids,H$counts,type="n",
    xaxt="n",
	main="Distribution of the Number of Types used in a Project", 
	xlab='Number of Types used in a Project', 
	ylab='Number of Projects', cex.main=0.75, cex.lab=0.75)
abline(v=breaks,col="lightgrey",lty=2)
abline(h=pretty(H$counts),col="lightgrey")
plot(H,add=T,freq=T,col="black")
#Creation X axis
axis(1, breaks,labels=breaks)
dev.off()


c100 <- 0
c90 <- 0
c80 <- 0
c70 <- 0
c60 <- 0
c50 <- 0
projects <- unique(csv[, "Project"])

for (i in projects){
	p <- csv[csv$Project == i,3]
	if (any(p==100)){
		c100 <- c100 + 1
	}
	if (any(p>=90)){
		c90 <- c90 + 1
	}
	if (any(p>=80)){
		c80 <- c80 + 1
	}
	if (any(p>=70)){
		c70 <- c70 + 1
	}
	if (any(p>=60)){
		c60 <- c60 + 1
	}
	if (any(p>=50)){
		c50 <- c50 + 1
	}
}

X <- c(c50, c60, c70, c80, c90, c100)
X <- X/length(projects)

jpeg(filename="lib_stats_count_authors_percent_per_project.jpg", width = 4, height = 4, units = 'in', res = 600)
plot(c(50, 60, 70, 80, 90, 100), X, type="l", col="blue",
	main="Percent of Projects that Contain an Author that Modified or\n Added more than X% of Types in the Project", 
	xlab='Percent of Types Modified or Added by an Author in Project', 
	ylab='Percent of Projects', cex.main=0.75, cex.lab=0.75)
dev.off()

##Go through each row and determine if a value is zero
row_sub <- apply(csv, 1, function(row) row[3] > 0.001 )

##Subset as usual
no_zero_csv <- csv[row_sub,]

summary(no_zero_csv)