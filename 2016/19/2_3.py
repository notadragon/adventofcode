#!/usr/bin/env python

import re, md5, sys, datetime, collections

part = 2

code=int(open("input").readlines()[0])
print code

elves = collections.deque(range(1,code+1))
print "%s: %s" % (datetime.datetime.now(),len(elves),)

currentElf = 0
while len(elves) > 1:
    numElves = len(elves)
    #print elves
    if numElves % 100000 == 0:
        print "%s: %s" % (datetime.datetime.now(),numElves,)

    halfway = numElves/2

    if part == 1:
        toRemove = (currentElf + 1) % numElves
    else:
        toRemove = (currentElf + halfway) % numElves

    
    while toRemove != 0:
        if toRemove < halfway:
            x = elves.popleft()
            elves.append(x)
            toRemove = toRemove - 1
            currentElf = (currentElf - 1) % numElves
        else:
            x = elves.pop()
            elves.appendleft(x)
            toRemove = (toRemove + 1) % numElves
            currentElf = (currentElf + 1) % numElves
            
    del elves[toRemove]
    if toRemove < currentElf:
        currentElf = currentElf % numElves
        continue
    else:
        currentElf = (currentElf + 1) % numElves

print elves
