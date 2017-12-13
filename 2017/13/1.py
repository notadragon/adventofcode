#!/usr/bin/env python

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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

vals={}
maxval = 0
lineRe = re.compile("(\\d+): (\\d+)")
for x in open(args.input).readlines():
    x = x.strip()
    m = lineRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
    else:
        vals[int(m.group(1))] = int(m.group(2))
        maxval = max(0,int(m.group(1)))
        
print "Vals: %s" % (vals,)

def severity(start):
    caught = 0
    sev = 0
    for depth in range(0,maxval+1):
        if depth in vals:
            scansize = vals[depth]
            if (start + depth) % (scansize * 2 - 2) == 0:
                sev += depth * scansize
                caught += 1
    return (caught,sev,)

if args.p1:
    print "Doing part 1"

    print "Severity: %s" % (severity(0)[1],)
            
if args.p2:
    print "Doing part 2"

    delay = 1
    while severity(delay)[0] != 0:
        if delay % 1000 == 0:
            print "Delay:%s" % (delay,)
        delay = delay + 1
    print "Safe delay: %s" % (delay,)
