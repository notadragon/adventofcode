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

lineRe = re.compile("[a-zA-Z]+")

data = []
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

#for d in data:
#    print(f"{d}")

def priority(x):
    if "a" <= x and x <= "z":
        return ord(x) - ord("a") + 1
    else:
        return ord(x) - ord("A") + 1 + 26
    

if args.p1:
    print("Doing part 1")

    def shared(d):
        l = len(d)//2
        c1 = d[0:l]
        c2 = d[l:]
        c1c = set([c for c in c1])
        c2c = set([c for c in c2])
        shareditems = c1c.intersection(c2c)
        return shareditems

    total = 0
    for d in data:
        sh = shared(d)
        for x in sh:
            p = priority(x)
            #print(f"{x} -> {p}")
            total += priority(x)
    print(f"{total}")
        
if args.p2:
    print("Doing part 2")

    total = 0
    for i in range(0,len(data),3):
        g = data[i:i+3]
        if not g:
            continue
        
        sets = [ set([c for c in d]) for d in g]
        c = sets[0].intersection(sets[1]).intersection(sets[2])
        print(f"{i}: {g} -> {c}")

        for x in c:
            total += priority(x)

    print(f"{total}")
