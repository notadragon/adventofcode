#!/usr/bin/env python

import argparse, operator, functools

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

def knot_hash(val):
    offsets = [ ord(x) for x in val ] + [17,31,73,47,23]

    skipsize = 0
    totalskip = 0

    vals = list(range(0,256))
    for p in range(0,64):
        for l in offsets:
            #print "Vals:%s" % (len(vals),)
            if l != 0:
                vals = list(reversed(vals[:l])) + vals[l:]

            toskip = (l + skipsize) % len(vals)

            vals = vals[toskip:] + vals[:toskip]
            skipsize = skipsize + 1
            totalskip += toskip

    remskip = len(vals) - (totalskip % len(vals))
    vals = vals[remskip:] + vals[:remskip]

    #print "Vals: %s" % (vals,)

    xors = [ functools.reduce(operator.xor,vals[i:i+16]) for i in range(0,len(vals),16) ]

    #print "Xors: %s" % (xors,)
    
    return "".join("%02x" % x for x in xors)

ival = open(args.input).readlines()[0].strip()

if args.p1:
    print "Doing part 1"

    if "sample" in args.input:
        vals = list(range(0,5))
    else:
        vals = list(range(0,256))
        
    skipsize = 0
    totalskip = 0
    for l in [ int(x) for x in ival.split(",") ]:
        if l != 0:
            vals = list(reversed(vals[:l])) + vals[l:]

        toskip = (l + skipsize) % len(vals)
        totalskip = (totalskip + toskip) % len(vals)

        vals = vals[toskip:] + vals[:toskip]

        skipsize = skipsize + 1

        
    remskip = len(vals) - (totalskip % len(vals))
    vals = vals[remskip:] + vals[:remskip]

    print "Vals: %s" % (vals,)

    print "p1: %s" % (vals[0] * vals[1],)

if args.p2:
    print "Doing part 2"

    print "Input: %s" % (ival,)
    print "Hash: %s" % (knot_hash(ival),)
