#!/usr/bin/env python

import re, md5

pinput = int(open("input").readlines()[0].strip())
#pinput = 10

pos = (1,1)

def isWall(loc):
    x = loc[0]
    y = loc[1]
    p = (x*x) + (3*x) + (2*x*y) + (y) + (y*y) + (pinput)
    #print "%s -> %s" % (loc,p,)
    bits = bin(p).count("1")
    return bits % 2 == 1

#print " 0123456789"
#for i in range(0,10):   
#    x = ["%s" % (i,),]
#    for j in range(0,10):
#        if isWall( (j,i) ):
#            x.append("#")
#        else:
#            x.append(" ")
#    print "".join(x)

distances = {pos:0}
ends = [pos,]
offsets = [ (1,0), (0,1), (-1,0), (0,-1), ]

finalpos = (31,39)

found = 1
maxd = 0
while maxd <= 50 and ends:
    nextends = []
    for x in ends:
        d = distances[x]
        for o in offsets:
            p = (o[0] + x[0],o[1] + x[1],)
            if p[0] < 0 or p[1] < 0:
                continue
            if p in distances:
                continue
            if isWall(p):
                distances[p] = d + 1
                continue
            distances[p] = d + 1
            maxd = max(d+1,maxd)
            if d+1 <= 50:
                found = found + 1
            nextends.append(p)
    ends = nextends
    print("distances: %s ends: %s" % (len(distances),len(nextends),))
    
print("Found:%s" % (found,))
            
