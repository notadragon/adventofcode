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

lineRe = re.compile("(forward|down|up) (\d+)")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( (m.group(1), int(m.group(2)), ) )

#for d in data:
#    print("%s" % (d,))
    
if args.p1:
    print("Doing part 1")

    loc = (0,0)
    for d in data:
        if d[0] == "up":
            loc = (loc[0], loc[1] - d[1],)
        elif d[0] == "down":
            loc = (loc[0], loc[1] + d[1],)
        elif d[0] == "forward":
            loc = (loc[0] + d[1], loc[1],)

    print("H,V: %s  p: %s" % (loc,loc[0] * loc[1],))
    
if args.p2:
    print("Doing part 2")

    loc = (0,0)
    aim = 0
    for d in data:
        if d[0] == "up":
            aim = aim - d[1]
        elif d[0] == "down":
            aim = aim + d[1]
        elif d[0] == "forward":
            loc = (loc[0] + d[1], loc[1] + aim * d[1],)
        #print(f"{d}: H: {loc[0]}  D: {loc[1]}  A: {aim}")

    print("H,V: %s  p: %s" % (loc,loc[0] * loc[1],))
