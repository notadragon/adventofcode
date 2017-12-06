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

    if b2[0] >= b1[0] and b2[1] <= b1[1]:
        del blocks[i+1]
        continue

    if b1[0] >= b2[0] and b1[1] <= b2[1]:
        del blocks[i]
        continue
    
    if b1[1] >= b2[0]-1:
        blocks[i] = (b1[0],b2[1],)
        del blocks[i+1]
        continue
    i = i + 1

total = 4294967296

unblocked = []

b = (0,blocks[0][0] - 1)
if b[1] - b[0] >= 0:
    unblocked.append(b)

for i in range(0,len(blocks)-1):
    b = (blocks[i][1]+1,blocks[i+1][0]-1)
    if b[1] - b[0] >= 0:
        unblocked.append(b)

b = (blocks[-1][1]+1,4294967295l)
if b[1]-b[0] >= 0:
    unblocked.append(b)

total = 0
for b in unblocked:
    print "%s:%s" % (b,b[1]-b[0]+1,)
    total += b[1] - b[0] + 1

print total

for i in range(0,len(unblocked)-1):
    if unblocked[i][1] >= unblocked[i+1][0]-1:
        print "WTF"

    
