#!/usr/bin/env python

import re

vowelRe=re.compile("(?:.*[aeiou]){3}.*")
doubleRe=re.compile(".*([a-z])\\1.*")
badRe=re.compile(".*(ab|cd|pq|xy).*")

total=0
nices=0
for line in open("input").readlines():
    line=line.strip()

    if not line:
        continue

    vm=bool(vowelRe.match(line))
    dm=bool(doubleRe.match(line))
    bm=bool(badRe.match(line))    

    nice=vm and dm and not bm
    
    print "line: %s v:%s d:%s b:%s nice:%s" % (line,vm,dm,bm,nice)

    total=total+1
    if nice:
        nices=nices+1

print "Lines: %i  Nice: %i" % (total,nices,)
