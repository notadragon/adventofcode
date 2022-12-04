#!/usr/bin/env pypy3

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

lineRe = re.compile("([0-9]+)-([0-9]+),([0-9]+)-([0-9]+).*")

data = []
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( ( (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))) )

#for d in data:
#    print(f"{d}")
    
if args.p1:
    print("Doing part 1")

    def contains(p1, p2):
        return p1[0] <= p2[0] and p1[1] >= p2[1]
    
    total = 0
    for d in data:
        p1 = d[0]
        p2 = d[1]
        if contains(p1,p2) or contains(p2,p1):
            total += 1
    print(f"{total}")
    
    
if args.p2:
    print("Doing part 2")

    def inside(p1,n):
        return n >= p1[0] and n <= p1[1]
    
    def overlaps(p1,p2):
        return inside(p1,p2[0]) or inside(p1,p2[1]) or inside(p2,p1[0]) or inside(p2,p1[1])
    
    total = 0
    for d in data:
        p1 = d[0]
        p2 = d[1]
        if overlaps(p1,p2):
            total += 1
    print(f"{total}")
