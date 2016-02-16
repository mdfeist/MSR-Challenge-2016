X11()

csv <- read.csv(file="libs_stats.csv",head=TRUE,sep=",")
summary(csv)

jpeg(filename="lib_stats_dist.jpg")
# Filled Density Plot
d <- density(csv$Percent.of.Libs.Used)
plot(d, 
	main="Density of Authors Versus Percent of Types Modified or Added", 
	xlab='Percent of Types Modified or Added by Author', 
	ylab='Density of Authors')
polygon(d, col="red", border="blue")
dev.off()

##Go through each row and determine if a value is zero
row_sub = apply(csv, 1, function(row) row[3] > 0.001 )

##Subset as usual
no_zero_csv = csv[row_sub,]

summary(no_zero_csv)