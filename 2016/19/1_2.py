#!/usr/bin/env python

import re, md5, sys, collections

code=int(open("input").readlines()[0])

print code

code = 5

elves = collections.deque(range(1,code+1))

def getToRemove(i,l):
    return i+1

currentPos = 0
while len(elves) > 1:
    print elves
    l = len(elves)

    toremove = getToRemove(currentPos,l) % l

    while toremove != 0:
        if toremove < l/2:
            torotate = elves[0:toremove]
            del elves[0:toremove]
            elves.extends(torotate)
            toremove = (toremove - len(torotate)) % l
            currentPos = (currentPos - len(torotate)) % 1
        else:
            torotate = elves[toremove:]
            del elves[toremove:]
            for x in torotate[-1:0:-1]:
                elves.appendleft(x)
            toremove = (toremove + len(torotate)) % l
            currentPos = (currentPos + len(torotate)) % l

    del elves[0]
