#!/usr/bin/env pypy

import argparse, re, itertools

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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

lineRe = re.compile("(.*) to (.*) = ([0-9]+)")

locations=set()
routes={}
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
    
    # Process input line
    routes[(m.group(1),m.group(2),)] = int(m.group(3))
    routes[(m.group(2),m.group(1),)] = int(m.group(3))
    locations.add(m.group(1))
    locations.add(m.group(2))
    
#print("Routes:%s" % (routes,))

def cost(routes,path):
    output = 0
    for i in range(0,len(path)-1):
        output += routes[ (path[i],path[i+1],) ]
    return output

if args.p1:
    print("Doing part 1")

    shortest = min( [cost(routes,path) for path in itertools.permutations(locations) ] )
    print("Shortest path: %s" % (shortest,))

        
if args.p2:
    print("Doing part 2")

    shortest = max( [cost(routes,path) for path in itertools.permutations(locations) ] )
    print("Longest path: %s" % (shortest,))
