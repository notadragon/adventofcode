#!/usr/bin/env python

import re

minchar='a'
maxchar='z'

badRe=re.compile(".*([iol]).*")

goodReStr = ".*(" + "|".join( [ chr(c) + chr(c+1) + chr(c+2) for c in range(ord(minchar),ord(maxchar)-1) ] ) + ").*"
goodRe=re.compile(goodReStr)
print goodReStr

goodRe2=re.compile(".*(.)\\1.*(.)\\2.*")

def check(pw):
    m = badRe.match(pw)
    if not goodRe.match(pw):
        return "Does not contain increasing triple."

    if m:
        return "Contains %s" % (m.group(1),)

    if not goodRe2.match(pw):
        return "Does not contain 2 pairs."
    
    return None

def increment(old,ndx=-1):
    ch=old[ndx]
    if ch == maxchar:
        if ndx + len(old) == 0:
            return (minchar,) + old[1:] 
        if ndx == -1:
            out=old[:ndx] + minchar
        else:
            out=old[:ndx] + minchar + old[ndx+1:]
        return increment(out,ndx-1)
    else:
        newch = chr(ord(ch)+1)
        if ndx == -1:
            return old[:ndx] + newch
        else:
            return old[:ndx] + newch + old[ndx+1:]

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    pw=line

    print "In: %s" % (pw,)
    increments=1
    found = 0
    pw = increment(pw)

    while True:
        result = check(pw)
        if result:
            if increments % 1000 == 0:
                print "Invalid (%i): %s (%s)" % (increments,pw,result,)
        else:
            found+=1
            print "Valid #%i (%i): %s" % (found,increments,pw,)

            if found > 5:
                break
            
        pw = increment(pw)
        increments+=1

