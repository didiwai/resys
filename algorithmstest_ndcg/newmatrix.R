a <- as.matrix(read.table("usermatrix.dat",sep=",",header=FALSE))


ta = t(a)

print("start compute path two")
l2 <- 0.25 * ta%*%a
r2 <- 0.25 * a%*%ta
print("start compute path three")
l3 <- 0.5 * a%*%l2
r3 <- 0.5 * ta%*%r2
#print("start compute path four")
#l4 <- ta%*%l3
#r4 <- a%*%r3
#print("start comput path five")
#l5 <- a%*%l4
#r5 <- ta%*%r4

print("start comput sum path")
#me <- l2
#write.table(me, file="topleft.txt", sep=",", col.names=F, row.names=F)
#mu <- ta + r3
#write.table(mu, file="topright.txt", sep=",", col.names=F, row.names=F)
um <- a + l3
write.table(um, file="downleft.txt", sep=",", col.names=F, row.names=F)
#uu <- r2
#write.table(uu, file="downright.txt", sep=",", col.names=F, row.names=F)

 
