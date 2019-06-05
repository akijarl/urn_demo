basefreq = c(0.4,0.3,0.2,0.1)
barplot(basefreq,
        col=c("cyan", "darkgreen", "orange", "magenta"),
        names.arg = c("A", "C","G","T"),
        ylab="Probability")

cumfreq = c(0, cumsum(basefreq))
colvec = c("cyan", "darkgreen", "orange", "magenta")
base.names = c("A", "C", "G", "T")

a.row = c(-0.886, 0.190, 0.633, 0.063)
c.row = c(0.253, -0.696, 0.127, 0.316)
g.row = c(1.266, 0.190, -1.519, 0.063)
t.row = c(0.253, 0.949, 0.127, -1.329)

q = matrix(c(a.row, c.row, g.row, t.row), nrow=4, ncol=4) 
taxis = seq(0, 5, by=0.005)

all.indices = c(1,2,3,4);
index = 1

for (index in c(1,2,3,4)) {
alt.bases = base.names[all.indices != index]
alt.indices = all.indices[all.indices != index]
curr.base = base.names[index]
curr.row = q[index,]
rate = -curr.row[index];
pos.rates = curr.row[curr.row > 0.0]
prob.cond.change = pos.rates/sum(pos.rates)
cumfreq = c(0, cumsum(prob.cond.change))

tag = paste("-", curr.base,  ".png", sep="")
den.tag = paste("prob-density", tag, sep="")
cum.prob.tag = paste("cumulative-prob", tag, sep="")
cum.prob.base.tag = paste("cumulative-prob-bases", tag, sep="")
png(den.tag)
plot(taxis, rate*exp(-rate*taxis), type="l", ylim=c(0, 2), bty="n",
     xlab = "waiting time", ylab="Probability density", xaxs="i", yaxs="i")
dev.off()

png(cum.prob.tag)
plot(taxis, 1 - exp(-rate*taxis), type="l", bty="n", ylim=c(0,1),
     xlab = "waiting time", ylab="Cumulative probability", xaxs="i", yaxs="i")
abline(h=1)
dev.off()

png(cum.prob.base.tag)
plot(c(0,1,2,3), cumfreq, pch=".", xaxt="n", ylim=c(0,1), xlim=c(0,3), yaxs="i",
     xlab="new base", ylab="Cumulative probability")
axis(1, at=0:3, labels=c("", base.names[alt.indices]))
rect(0, cumfreq[1], 1, cumfreq[2], col=colvec[alt.indices[1]])
rect(0, cumfreq[2], 2, cumfreq[3], col=colvec[alt.indices[2]])
rect(0, cumfreq[3], 3, cumfreq[4], col=colvec[alt.indices[3]])
abline(h=c(0,1))
dev.off()
} # end for

