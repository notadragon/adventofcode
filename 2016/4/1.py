#!/usr/bin/env python

import re

roomRE=re.compile("^([a-z-]+)+-([0-9]+)\\[([a-z]+)\\]$")

def decriptChar(c,sectorId):
    if c == "-":
        return " "

    i = (ord(c)-ord("a") + sectorId) % 26
    return chr(ord("a") + i)
    

def decript(roomId,sectorId):
    return "".join(decriptChar(c,sectorId) for c in roomId)

total = 0
for x in open("input").readlines():
    m = roomRE.match(x)
    roomId = m.group(1)
    sectorId = int(m.group(2))
    cksum = m.group(3)
    
    print "roomId:%s sectorId:%s cksum:%s" % (roomId,sectorId,cksum,)

    counts={}
    for c in roomId:
        if c == "-":
            continue
        if counts.has_key(c):
            counts[c] = counts[c] + 1
        else:
            counts[c] = 1
    ordered = []
    for (l,c) in counts.items():
        ordered.append( (-c,l) )

    ordered.sort()
    
    realcksum="".join(x[1] for x in ordered[0:5])

    if cksum == realcksum:
        good=True
    else:
        good=False
        
    print " ordered: %s cksum: %s good:%s" % (ordered,realcksum,good,)

    if good:
        total = total + sectorId

    print " decripted: %s" % (decript(roomId,sectorId,))
        
print "Good total: %s" % (total,)
