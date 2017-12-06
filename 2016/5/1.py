#!/usr/bin/env python

import re, md5


code=open("input").readlines()[0].strip()
print code

chars=[None,None,None,None,None,None,None,None]
i = 0
rem = 8

while rem > 0:
    if i % 1000000 == 0:
        print i
    
    m = md5.new()
    m.update("%s%s" % (code,i,))
    h = m.hexdigest()

    if h[0] == "0" and h[1] == "0" and h[2] == "0" and h[3] == "0" and h[4] == "0":
        if h[5] >= "0" and h[5] <= "8":
            ndx = int(h[5])
            if chars[ndx]:
                continue

            chars[ndx] = h[6]
            rem = rem - 1
            print "Found %s: c[%s]=%s" % (i,h[5],h[6])

    i = i + 1


print "Password: %s" % ("".join(chars),)
    
