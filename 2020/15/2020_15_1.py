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

lineRe = re.compile(".*")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data = [ int(y) for y in x.split(",") ]

print("Data: %s" % (data,))

def numbers(data):

    indices = {}
    diffs = {}
    
    for i in range(0,len(data)):
        last = data[i]
        if last in indices:
            diffs[last] = i - indices[last]
        indices[last] = i
        yield last

    pos = len(data)
    while True:
        if last in diffs:
            next = diffs[last]
        else:
            next = 0

        last = next
        if last in indices:
            diffs[last] = pos - indices[last]
        indices[last] = pos

        pos = pos + 1
        yield last


if args.p1:
    print("Doing part 1")

    x = numbers(data)
    v = None
    
    for i in range(0,2020):
        v = x.next()
        #print("%s:%s" % (i+1,v,))
    print("%s:%s" % (2020, v,) )
    
if args.p2:
    print("Doing part 2")

    x = numbers(data)
    v = None
    
    for i in range(0,30000000):
        v = x.next()
        #print("%s:%s" % (i+1,v,))
        
    print("%s:%s" % (30000000, v,) )
