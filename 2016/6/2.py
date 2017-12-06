#!/usr/bin/env python

import re, md5

freqs = [{},{},{},{},{},{},{},{}]

for x in open("input").readlines():
    x = x.strip()
    for i in range(0,8):
        c=x[i:i+1]
        if freqs[i].has_key(c):
            freqs[i][c] = freqs[i][c]+1
        else:
            freqs[i][c]=1

out = []
for f in freqs:
    x=[]
    for (k,c) in f.items():
        x.append( (-c,k) )
    x.sort()
    out.append(x[len(x)-1][1])

print "".join(out)
            
    
