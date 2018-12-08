#!/usr/bin/env python

import re

re1=re.compile(".*([a-z]{2}).*\\1.*")
re2=re.compile(".*([a-z]).\\1.*")

total=0
nices=0
for line in open("input").readlines():
    line=line.strip()

    if not line:
        continue

    m1=bool(re1.match(line))
    m2=bool(re2.match(line))

    nice=m1 and m2
    
    print "line: %s m1:%s m2:%s nice:%s" % (line,m1,m2,nice)

    total=total+1
    if nice:
        nices=nices+1

print "Lines: %i  Nice: %i" % (total,nices,)
