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

lineRe = re.compile("^(?:([A-Z]+)|(?:([A-Z]+) -> ([A-Z])))$")

insertions = {}
template = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    
    if m.group(1):
        template = x
    else:
        if m.group(2) in insertions:
            print("WTF")
        insertions[m.group(2)] = m.group(3) 

print(f"Template: {template}")
        
def doPairInsertion(prev):
    data = []

    for i in range(0,len(prev)):
        data.append(prev[i])
        key = prev[i:i+2]
        if key in insertions:
            data.append(insertions[key])

    return "".join(data)

def score(elements):
    counts = {}
    for c in elements:
        if c not in counts:
            counts[c] = 1
        else:
            counts[c] = counts[c] + 1
    maxc = max(counts.values())
    minc = min(counts.values())
    return maxc - minc;

def makeBreakdown(elements):
    pairs = {}
    for i in range(0, len(elements)-1):
        key = elements[i:i+2]
        if key in pairs:
            pairs[key] = pairs[key+1]
        else:
            pairs[key] = 1
    return ( elements[0], pairs, elements[-1],)


def doBreakdownInsertion(breakdown):
    newpairs = {}
    for key,count in breakdown[1].items():
        if key in insertions:
            ival = insertions[key]

            leftkey = key[0] + ival
            newpairs[leftkey] = newpairs.get(leftkey,0) + count
            
            rightkey = ival + key[1]
            newpairs[rightkey] = newpairs.get(rightkey,0) + count
        else:
            newpairs[key] = newpairs.get(key,0) + count
    return (breakdown[0], newpairs, breakdown[2],)

def breakdownCounts(breakdown):
    counts = {}
    counts[breakdown[0]] = counts.get(breakdown[0],0) + 1
    for key,count in breakdown[1].items():
        counts[key[0]] = counts.get(key[0],0) + count
        counts[key[1]] = counts.get(key[1],0) + count
    counts[breakdown[2]] = counts.get(breakdown[2],0) + 1
    return { key : count//2 for key,count in counts.items() }

if args.p1:
    print("Doing part 1")

    elements = template
    for i in range(0,10):
        elements = doPairInsertion(elements)

    print(f"Final Score: {score(elements)}")

    breakdown = makeBreakdown(template)
    #print(f"Initial Breakdown: {breakdown}")

    for i in range(0,10):
        breakdown = doBreakdownInsertion(breakdown)

    #print(f"Final Breakdown: {breakdown}")
    counts = breakdownCounts(breakdown)
    #print(f"Final Counts: {counts}")

    score = max(counts.values()) - min(counts.values())
    print(f"Final (breakdown) Score: {score}")
    
if args.p2:
    print("Doing part 2")

    breakdown = makeBreakdown(template)
    #print(f"Initial Breakdown: {breakdown}")

    for i in range(0,40):
        breakdown = doBreakdownInsertion(breakdown)

    #print(f"Final Breakdown: {breakdown}")
    counts = breakdownCounts(breakdown)
    #print(f"Final Counts: {counts}")

    score = max(counts.values()) - min(counts.values())
    print(f"Final (breakdown) Score: {score}")
    
