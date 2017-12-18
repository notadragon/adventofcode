#!/usr/bin/env pypy

import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

ival = int(open(args.input).readlines()[0])

print "Ival: %s" % (ival,)

if args.p1:
    print "Doing part 1"

    nextval = 1
    buf = [0]
    pos = 0

    for i in range(0,2017):
        newpos = (pos + ival) % len(buf)
        buf = buf[:newpos+1] + [nextval] + buf[newpos+1:]
        pos = newpos + 1
        nextval = nextval + 1

        #print ",".join( [ ("(%s)" % (buf[i],)) if (i == pos) else (str(buf[i])) for i in range(0,len(buf)) ] )

    print ",".join( [ ("(%s)" % (buf[i],)) if (i == pos) else (str(buf[i])) for i in range(pos-4,pos+4) ])

        
if False:
    print "Doing part 2"

    nextval = 1
    buf = [0]
    pos = 0

    for i in range(0,50000000):
        if (i % 1000000) == 0:
            print "Iter: %s" % (i,)
        newpos = (pos + ival) % len(buf)
        buf = buf[:newpos+1] + [nextval] + buf[newpos+1:]
        pos = newpos + 1
        nextval = nextval + 1

        #print ",".join( [ ("(%s)" % (buf[i],)) if (i == pos) else (str(buf[i])) for i in range(0,len(buf)) ] )

    zpos = buf.indexof(0)
    
    print ",".join( [ ("(%s)" % (buf[i],)) if ((i % len(buf)) == pos) else (str(buf[i])) for i in range(zpos-4,zpos+4) ])

if args.p2:
    print "Doing part 2"

    # initialize at step 1, 0,(1)
    pos = 1
    # buf = [0,1]
    nextval = 2
    after0 = 1
    buflen = 2
    zpos = 0
    
    while nextval < 50000000:
        newpos = (pos + ival) % buflen

        if zpos == newpos:
            after0 = nextval
        elif zpos > newpos:
            zpos = zpos + 1
        buflen = buflen + 1
            
        pos = newpos + 1
        nextval = nextval + 1
        
    print "pos: %s zpos: %s nextval: %s buflen: %s after0: %s" % (pos, zpos, nextval, buflen, after0,)
