#!/usr/bin/env pypy

import argparse, re, itertools, collections

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

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("(-?[0-9]+),(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)")

stars = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    stars.append( (int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),) )

#for star in stars:
#    print("Input: %s" % (star,))

def mdistance(l1,l2):
    return sum([ abs(a-b) for a,b in zip(l1,l2) ])

if args.p1:
    print("Doing part 1")

    constellations = { s1:set([s1,]) for s1 in stars }
    
    for i in range(0,len(stars)):
        s1 = stars[i]
        for  j in range(i+1,len(stars)):
            s2 = stars[j]

            if mdistance(s1,s2) <= 3:
                #print(" %s <-> %s" % (s1,s2,))

                c1 = constellations[s1]
                c2 = constellations[s2]

                if c1 != c2:
                    for cs1 in c1:
                        constellations[cs1] = c2
                        c2.add(cs1)

    allc = set([ tuple(c) for c in constellations.values() ])

    print("# of constellations: %s" % (len(allc,),))
    
if args.p2:
    print("Doing part 2")
