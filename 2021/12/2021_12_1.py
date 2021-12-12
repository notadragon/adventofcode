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

lineRe = re.compile("([a-zA-Z]+)-([a-zA-Z]+).*")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( (m.group(1),m.group(2),))


connections = {}
for f,t in data:
    if f not in connections:
        connections[f] = set()
    connections[f].add(t)
    if t not in connections:
        connections[t] = set()
    connections[t].add(f)

def paths(connections, omit, prevpath, end):
    if prevpath[-1] == end:
        yield prevpath
        return

    for n in connections[prevpath[-1]]:
        if n in omit:
            continue

        npath = prevpath + (n,)

        if n.lower() == n:
            nomit = set(omit)
            nomit.add(n)
        else:
            nomit = omit

        for p in paths(connections, nomit, npath, end):
            yield p
    
if args.p1:
    print("Doing part 1")

    allpaths = set()
    for p in paths(connections, set(["start"]), ("start",), "end"):
        allpaths.add(p)

    #for p in allpaths:
    #    print(f"{p}")

    print(f"Total paths: {len(allpaths)}")
    
def paths2(connections, omit, doubled, prevpath, end):
    if prevpath[-1] == end:
        yield prevpath
        return

    for n in connections[prevpath[-1]]:
        if n == "start":
            continue
        
        if doubled and (n in omit):
            continue

        npath = prevpath + (n,)

        if n.lower() == n:
            if n in omit:
                ndoubled = True
                nomit = omit
            else:
                ndoubled = doubled
                nomit = set(omit)
                nomit.add(n)
        else:
            ndoubled = doubled
            nomit = omit

        for p in paths2(connections, nomit, ndoubled, npath, end):
            yield p
    
    
if args.p2:
    print("Doing part 2")

    allpaths = set()
    for p in paths2(connections, set(["start"]), False, ("start",), "end"):
        allpaths.add(p)

    #for p in allpaths:
    #    print(f"{p}")

    print(f"Total paths: {len(allpaths)}")
    
