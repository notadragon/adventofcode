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

ival =  open(args.input).readlines()[0].strip()

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
    
print "Ival: %s" % (ival,)

#for x in [ "", "AoC 2017", "1,2,3", "1,2,4", ] :
#    print "x: %s" % (x,)
#    print "hash: %s" % (knot_hash(x),)

grid = []
    
for i in range(0,128):
    key = "%s-%s" % (ival,i,)
    hash = knot_hash(key)
    bits = "".join([ bin(int(x,16))[2:].zfill(4) for x in hash ])
    grid.append(bits)
    
if args.p1:
    print "Doing part 1"

    used = 0
    for g in grid:
        for x in g:
            if x == "1":
                used = used + 1
    print "Used: %s" % (used,)

if args.p2:
    print "Doing part 2"

    newgrid = [ list(x) for x in grid ]


    def fillgrid(x,y,g):
        toclear = [ (x,y) ]
        while toclear:
            loc = toclear.pop()
            if g[loc[0]][loc[1]] == '1':
                g[loc[0]][loc[1]] = '0'
                if loc[0] > 0: toclear.append( (loc[0]-1,loc[1]) )
                if loc[0] < len(g)-1: toclear.append( (loc[0]+1,loc[1]) )
                if loc[1] > 0: toclear.append( (loc[0],loc[1]-1) )
                if loc[1] < len(g)-1: toclear.append( (loc[0],loc[1]+1) )

    regions = 0
    for x in range(0,128):
        for y in range(0,128):
            gval = newgrid[x][y]
            if gval == '1':
                fillgrid(x,y,newgrid)
                regions = regions + 1
    print "Regions: %s" % (regions,)
            
