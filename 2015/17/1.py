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
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("[0-9]+")
values = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    values.append(int(x))

values.sort()
values.reverse()
print("Values: %s" % (values,))

def fillcontainers(containers,i,total):
    if i == len(containers)-1:
        if total == containers[i]:
            yield (containers[i],)
        return
    for rest in fillcontainers(containers,i+1,total):
        yield rest
    if containers[i] == total:
        yield (containers[i],)
    elif containers[i] < total:
        for rest in fillcontainers(containers,i+1,total-containers[i]):
            yield (containers[i],) + rest

if args.p1:
    print("Doing part 1")

    print("variatons:%s" % ( sum([ 1 for s in fillcontainers(values,0,150) ] ), ) )
    
if args.p2:
    print("Doing part 2")

    numcontainers = len(values)+1
    variations = 0
    for s in fillcontainers(values,0,150):
        if len(s) < numcontainers:
            numcontainers = len(s)
            variations = 1
        elif len(s) == numcontainers:
            variations += 1

    print("Min containers: %s" % (numcontainers,))
    print("Variations:%s" % (variations,))
          
            
