#!/usr/bin/env python

import re

lights={}

actionRe=re.compile("(turn on|turn off|toggle) (\\d+),(\\d+) through (\\d+),(\\d+)")

for x in range(0,1000):
    for y in range(0,1000):
        lights[(x,y)]=False

for line in open("input").readlines():
    line=line.strip()
    if not line: continue

    m=actionRe.match(line)

    if not m:
        print "Invalid line:%line"

    action=m.group(1)
    fromLoc=(int(m.group(2)),int(m.group(3)),)
    toLoc=(int(m.group(4)),int(m.group(5)),)

    for x in range(fromLoc[0],toLoc[0]+1):
        for y in range(fromLoc[1],toLoc[1]+1):
            loc=(x,y)
            if action == "turn on":
                lights[loc] = True
            elif action == "turn off":
                lights[loc] = False
            else:
                lights[loc] = not lights[loc]
                
    print "line:%s %s from %s to %s" % (line,action,fromLoc,toLoc,)


numOn=0
for x in range(0,1000):
    for y in range(0,1000):
        if lights[(x,y)]:
            numOn = numOn + 1

print "Lights On:%s" % (numOn,)
