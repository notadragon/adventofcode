#!/usr/bin/env python

import re, md5, sys

code=int(open("input").readlines()[0])

print code

elves = [1] * code

lastStanding = None
currentElf = 0

maxx = 1
print("Max: %s num:%s" % (maxx,len(elves),))

while lastStanding == None:

    x = elves[currentElf]
    if x == 0:
        currentElf = (currentElf + 1) % (len(elves))
        continue

    nextElf = -1
    for i in xrange(1,len(elves)):
        n = (currentElf + i) % (len(elves))
        if elves[n] > 0:
            nextElf = n
            break
    if nextElf < 0:
        lastStanding = currentElf
    else:
        elves[currentElf] =  x + elves[nextElf]
        elves[nextElf] = 0

        if elves[currentElf] > maxx:
            maxx = elves[currentElf]
            print("Max: %s" % (maxx,))

        currentElf = (nextElf + 1) % len(elves)


print "Last Standing: %s" % (lastStanding+1,)

        
    
