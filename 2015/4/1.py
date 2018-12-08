#!/usr/bin/env pypy

import argparse, re
import md5

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True
    args.p2 = True

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    ival = x

print("Ival: %s" % (ival,))

def dohash(i):
    hashinput = "%s%i" % (ival,i)
    m=md5.new()
    m.update(hashinput)
    return "".join([ "{:02X}".format(ord(b)) for b in m.digest()  ])

if args.p1:
    print("Doing part 1")

    i = 0
    while True:
        mhash = dohash(i)

        if mhash.startswith("00000"):
            print("%s -> %s" % (i,mhash,))
            break
        
        i = i + 1
    
if args.p2:
    print("Doing part 2")

    i = 0
    while True:
        mhash = dohash(i)

        if mhash.startswith("000000"):
            print("%s -> %s" % (i,mhash,))
            break
        
        i = i + 1
