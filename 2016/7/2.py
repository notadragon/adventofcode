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

    abas = []
    for i in range(0,len(x),2):
        ip1=x[i]
        for j in range(0,len(ip1)-2):
            if ip1[j] == ip1[j+2] and ip1[j] != ip1[j+1]:
                abas.append(ip1[j:j+2])
    hasBab = False
    for i in range(1,len(x),2):
        for aba in abas:
            bab = aba[1] + aba[0] + aba[1]
            if bab in x[i]:
                print "Good bab: %s" % (bab,)
                hasBab = True

    if hasBab:
        print l
        goodAddrs += 1


print "Good: %s" % (goodAddrs,)
