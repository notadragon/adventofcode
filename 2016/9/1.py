#!/usr/bin/env python

import re, md5

markerRe = re.compile("\(([0-9]+)x([0-9]+)\)")

for l in open("input").readlines():
    l = l.strip()

    out = ""
    while len(l) > 0:
        m = markerRe.search(l)
        if m:
            start = m.start()
            end = m.end()
            
            out = out + l[0:start]

            mlen = int(m.group(1))
            mnum = int(m.group(2))
            marked = l[end:end+mlen]

            l = l[end+mlen:]

            for i in range(0,mnum):
                out = out + marked

        else:
            out = out + l
            l = ""

    print out
    print len(out)
