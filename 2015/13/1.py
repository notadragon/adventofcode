#!/usr/bin/env python

import re, itertools

lineRe = re.compile("(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)")

people=set()
people.add("Me")

happinesses={}
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)
        continue
    
    p1=m.group(1)
    p2=m.group(4)
    h=int(m.group(3))
    if m.group(2) == "lose": h=-h

    people.add(p1)
    people.add(p2)

    happinesses[(p1,p2)] = h
    
print "People: %s" % (people,)


maxPerm = None
maxTotal = 0
for p in itertools.permutations(people):
    total=0
    toprint=[]
    for x in range(-1,len(p)-1):
        h1 = happinesses.get( (p[x],p[x+1],), 0)
        h2 = happinesses.get( (p[x+1],p[x],), 0)
        toprint.append( (h1,h2) )
        total += h1
        total += h2
        
    if maxPerm == None or total > maxTotal:
        maxPerm = p
        maxTotal = total

        print "%s %s: %s" % (p,toprint,total,)
        
