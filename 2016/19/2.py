#!/usr/bin/env python

import re, md5, sys

code=int(open("input").readlines()[0])

print code

elves = range(1,code+1)

currentElf = 0
while len(elves) > 1:
    if len(elves) % 100000 == 0:
        print len(elves)
        
    oppositeElf = (currentElf + (len(elves)/2)) % len(elves)
    del elves[oppositeElf]
    if oppositeElf < currentElf:
        continue
    else:
        currentElf = (currentElf + 1) % len(elves)

print elves
