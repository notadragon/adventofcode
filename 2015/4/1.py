#!/usr/bin/env python

import md5

key=open("input").readlines()[0].strip()
print "Key:%s" % (key,)

prefix="000000"

i=1
done=False
while True:
    m=md5.new()
    input="%s%i" % (key,i,)
    m.update(input)
    md5sum="".join([ "{:02X}".format(ord(b)) for b in m.digest()  ])

    if md5sum[0:len(prefix)]==prefix:
        done=True

    if done or i % 10000 == 0:
        print "I:%d Input:%s md5:%s" % (i,input,md5sum,)

    if done:
        break
    i=i+1
