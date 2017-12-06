#!/usr/bin/env python

import re, md5

a=open("input").readlines()[0]

def step(a):
    b=""
    for i in range(len(a)-1,-1,-1):
        if a[i] == "0":
            b = b + "1"
        else:
            b = b + "0"
    return a + "0" + b

def checksumstep(x):
    out = ""
    for i in range(0,len(x),2):
        if i+1 == len(x):
            out = out + "0"
        elif x[i] == x[i+1]:
            out = out + "1"
        else:
            out = out + "0"
    return out

def checksum(x):
    out = checksumstep(x)
    while len(out) % 2 == 0:
        out = checksumstep(out)
    return out

def fill(a,l):
    while len(a) < l:
        a = step(a)
    return a

f = fill(a,272)[0:272]

print "Fill (%s):%s" % (len(f),f,)
print len(f)

c = checksum(f)
print "checksum:%s" % (c,)
