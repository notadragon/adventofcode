#!/usr/bin/env python

import re, md5

lineRe = re.compile("/dev/grid/node-x([0-9]+)-y([0-9]+) +([0-9]+)T +([0-9]+)T +([0-9]+)T +([0-9]+)%")

nodes={}

for l in open("input").readlines()[2:]:
    l = l.strip()
    m = lineRe.match(l)
    if m:
        x=int(m.group(1))
        y=int(m.group(2))
        size=int(m.group(3))
        used=int(m.group(4))
        avail=int(m.group(5))
        usedpct=int(m.group(6))
        nodes[ (x,y) ] = (x,y,size,used,avail,usedpct,)
        continue
    print l

viable = 0
    
for a in nodes.values():
    for b in nodes.values():
        if a[0] == b[0] and a[1] == b[1]:
            continue
        if a[3] == 0:
            continue
        if a[3] > b[4]:
            continue
        print " %s %s" % (a,b,)
        viable=viable+1

print "viable:%s" % (viable,)
