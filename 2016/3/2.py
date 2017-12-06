#!/usr/bin/env python

import re

possible = 0
total = 0

t1=[]
t2=[]
t3=[]

for x in open("input").readlines():
    s1 = int(x[0:5])
    s2 = int(x[5:10])
    s3 = int(x[10:])

    t1.append(s1)
    t2.append(s2)
    t3.append(s3)
    
    if len(t1) == 3:
        for t in (t1,t2,t3,):
            total = total + 1
            s1=t[0]
            s2=t[1]
            s3=t[2]
            if s1 + s2 <= s3:
                continue
            if s1 + s3 <= s2:
                continue
            if s2 + s3 <= s1:
                continue
            possible = possible + 1

        t1 = []
        t2 = []
        t3 = []

print "%s / %s" % (possible, total, )
    
    
