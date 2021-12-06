#!/usr/bin/env python3

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

lineRe = re.compile("\d+(,\d+)*")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data = [ int(y) for y in x.split(",") ]

print(f"Data: {data}")


if False:
    def step(counts):
        born = 0
        for c in counts:
            if c == 0:
                yield 6
                born = born + 1
            else:
                yield c - 1
        for i in range(0,born):
            yield 8

    counts = data
    print(f"Initial state: {counts}")
    for i in range(0,18):
        counts = list(step(counts))
        print(f"After {i+1} days: {counts}")

def daypop(data,days):
    counts = [0] * 9
    for d in data:
        counts[d] = counts[d] + 1

    def step(counts):
        born = counts[0]
        newcounts = counts[1:] + [born,]
        newcounts[6] += born
        return newcounts

    print(f"{counts}")
    for i in range(0,days):
        counts = step(counts)
        print(f"{counts}")
        
    pop = sum(counts)
    print(f"Population: {pop}")

        
if args.p1:
    print("Doing part 1")

    daypop(data,80);
    
    
if args.p2:
    print("Doing part 2")

    daypop(data,256);
