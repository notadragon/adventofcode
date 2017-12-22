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

mappings = {}
lineRe = re.compile("(.*) => (.*)")
for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
        continue
    
    mfrom = tuple(m.group(1).split("/"))
    mto = tuple(m.group(2).split("/"))

    mappings[mfrom] = mto
    
start = (".#.","..#","###")

def rotate(m):
    out = tuple((
        "".join((m[i][j] for i in range(len(m)-1,-1,-1)))
        for j in range(0,len(m))))
            
    return tuple(out)

print "Start:"
for x in start: print x

print "Rotated start:"
for x in rotate(start): print x

allmappings = {}
for mfrom,mto in mappings.items():
    fmfrom = tuple(("".join(reversed(x)) for x in mfrom))
    for i in range(0,4):
        allmappings[mfrom] = mto
        allmappings[fmfrom] = mto
        mfrom = rotate(mfrom)
        fmfrom = rotate(fmfrom)
    

print "Mappings: %s -> %s" % (len(mappings),len(allmappings),)

def expand(m,steps):
    em = []
    
    for i in range(0,len(m),steps):
        emrow = []
        em.append(emrow)
        for j in range(0,len(m),steps):
            broken = tuple(( m[i+y][j:j+steps] for y in range(0,steps)))
            expanded = allmappings[broken]
            if not expanded:
                print "No expansion for: %s" % (broken,)
                return None
            emrow.append(expanded)

    out = []
    for emrow in em:
        for i in range(0,steps+1):
            out.append("".join(x[i] for x in emrow))
            
    return tuple(out)

counts = []

if args.p1 or args.p2:
    print "Doing part 1"

    def stepgrid(m):
        if len(m) % 2 == 0:
            return expand(m,2)
        elif len(m) % 3 == 0:
            return expand(m,3)
        else:
            return None

    s = start
    i = 0
    while s:
        s = stepgrid(s)
        i = i + 1
        print "I: %s" % (i,)
        if s:
            #for x in s:
            #    print "  %s" % (x,)
            c = sum(x.count("#") for x in s)
            counts.append(c)
            #print "  on: %s" % (c,)

        if i == 18:
            break

    print "Counts: %s" % (counts,)
