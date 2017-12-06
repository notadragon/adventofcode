#!/usr/bin/env python

import re, md5, sys

markerRe = re.compile("\(([0-9]+)x([0-9]+)\)")

for l in open("input2").readlines():
    total = 0
    l = l.strip()

    i = 0
    while True:
        i = i + 1
        m = markerRe.search(l)
        if not m:
            total = total + len(l)
            l = ""
            break

        start = m.start()
        end = m.end()

        mlen = int(m.group(1))
        mnum = int(m.group(2))
        marked = l[end:end+mlen]

        l = (mnum*marked) + l[end+mlen:]

        total = total + start

        if i % 100000 == 0:
            print("total:%s rem:%s" % (total,len(l),))

    print("Total:%s" % ( total,))
