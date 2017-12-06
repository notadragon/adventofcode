#!/usr/bin/env python

import re, md5

lineRe = re.compile("([0-9]+)-([0-9]+)")

blocks = []

for l in open("input").readlines():
    l = l.strip()
    m = lineRe.match(l)
    if m:
        i = int(m.group(1))
        j = int(m.group(2))
        
        blocks.append( (i,j) )
        
        continue
    
    print l

blocks.sort()
i = 0
while i < len(blocks)-1:
    b1 = blocks[i]
    b2 = blocks[i+1]
    if b1[1] >= b2[0]-1:
        blocks[i] = (b1[0],b2[1],)
        del blocks[i+1]
        continue
    i = i + 1

total = 4294967296
    
for b in blocks:
    total = total - (b[1] - b[0] + 1)

print total


    
