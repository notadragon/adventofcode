#!/usr/bin/env python

import re, md5

tripleRe = re.compile(".*(.)\\1\\1.*")
quintRe = re.compile(".*(.)\\1\\1\\1\\1.*")

salt = open("input").readlines()[0].strip()

i = 0

keys = []

candidates = {}

def dohash(i):
    pw="%s%s" % (salt,i,)
    m = md5.new()
    m.update(pw)
    return m.hexdigest()

def dohash(i):
    pw="%s%s" % (salt,i,)
    m = md5.new()
    m.update(pw)

    out = m.hexdigest()
    
    for i in range(0,2016):
        m = md5.new()
        m.update(out)
        out = m.hexdigest()

        
    return out

def findTriple(s):
    for i in range(0,len(s)-2):
        if s[i] == s[i+1] and s[i] == s[i+2]:
            return s[i]
    return None

def findQuint(s):
    for i in range(0,len(s)-4):
        if s[i] == s[i+1] and s[i] == s[i+2] and s[i] == s[i+3] and s[i] == s[i+4]:
            return s[i]
    return None

while len(keys) < 80:
    h = dohash(i)

    print "%s -> %s" % (i,h,)
    
    done = []
    for ndx,k,rs in candidates.values():
        if ndx + 1000 < i:
            done.append(ndx)
        else:
            if rs in h:
                keys.append( (ndx,k,i,h,rs) )
                done.append(ndx)
    for ndx in done:
        del candidates[ndx]

    r = findTriple(h)
    if r:
        #print "  match: %s : %s" % (h,r,)
        candidates[i] = (i,h,r*5)

    i = i + 1

keys.sort()
x = 1
for k in keys:
    if k[2] <= k[0] or k[2] > k[0] + 1000:
        print "FAIL (key range):%s" % (k,)

    h = dohash(k[0])
    m = tripleRe.match(h)
    if not m:
        print "FAIL (Not triple):%s" % (k,)

    r = findTriple(h)
    if not r:
        print "FAIL (findTriple):%s" % (k,)

    h2 = dohash(k[2])
    if not r*5 in h2:
        print "FAIL:%s" % (k,)

    m = quintRe.match(h2)
    if not m:
        print "FAIL:%s" % (k,)

    if r != m.group(1)[0]:
        print "FAIL:%s" % (k,)
        
    print "%s: %s" % (x,k,)
    x = x + 1

print max( [ a[0] for a in keys[0:64] ] )
