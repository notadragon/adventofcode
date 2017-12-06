#!/usr/bin/env python

import re, md5

lineRe = re.compile("Disc #([0-9]+) has ([0-9]+) positions; at time=([0-9]+), it is at position ([0-9]+)")

disks = []

for l in open("input").readlines():
    l = l.strip()

    m = lineRe.match(l);
    if m:
        discId = int(m.group(1))
        numPos = int(m.group(2))
        t = int(m.group(3))
        pos = int(m.group(4))
        disks.append( (discId,numPos,pos) )
        continue
        
    print l

disks.append( (len(disks)+1,11,0,) )


print disks

t = -1
while True:
    t = t + 1

    good = True
    for (discId,numPos,startPos) in disks:
        passPos = (startPos + discId + t) % (numPos)
        #print "%s:%s:%s:%s" % (t,discId,numPos,passPos,)
        if passPos != 0:
            good = False

    if good:
        break

print t
