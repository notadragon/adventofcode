#!/usr/bin/env python

import re, md5

def containsAbba(s):
    for i in range(0,len(s)-3):
        if s[i] == s[i+3] and s[i] != s[i+1] and s[i+1] == s[i+2]:
            return True

    return False

re1=re.compile("[\[\]]");

goodAddrs = 0
for l in open("input").readlines():
    l = l.strip()

    x = re1.split(l)

    hasAbba = False
    hasBadAbba = False
    for i in range(0,len(x),2):
        if containsAbba(x[i]):
            hasAbba = True
    for i in range(1,len(x),2):
        if containsAbba(x[i]):
            hasBadAbba = True

    if hasAbba and not hasBadAbba:
        print l
        goodAddrs += 1


print "Good: %s" % (goodAddrs,)
