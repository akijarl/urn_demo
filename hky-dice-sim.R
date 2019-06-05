basefreq = c(0.4,0.3,0.2,0.1)
barplot(basefreq,
        col=c("cyan", "darkgreen", "orange", "magenta"),
        names.arg = c("A", "C","G","T"),
        ylab="Probability")

cumfreq = c(0, cumsum(basefreq))