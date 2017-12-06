#!/usr/bin/env python

import re, md5, sys, datetime, collections

code=int(open("input").readlines()[0])
print code

elves = collections.deque(range(1,code+1))
print "%s: %s" % (datetime.datetime.now(),len(elves),)

currentElf = 0
while len(elves) > 1:
    #print elves
    if len(elves) % 100000 == 0:
        print "%s: %s" % (datetime.datetime.now(),len(elves),)
        
    oppositeElf = (currentElf + (len(elves)/2)) % len(elves)

    #print "  %s steals from %s" % (elves[currentElf],elves[oppositeElf],)
    
    del elves[oppositeElf]
    if oppositeElf < currentElf:
        currentElf = currentElf % len(elves)
        continue
    else:
        currentElf = (currentElf + 1) % len(elves)

print elves
