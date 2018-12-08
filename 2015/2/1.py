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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

lineRe = re.compile("([0-9]+)x([0-9]+)x([0-9]+)")
vals=[]
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue

    vals.append( (int(m.group(1)), int(m.group(2)), int(m.group(3)),) )

#print("Vals: %s" % (vals,))

if args.p1:
    print("Doing part 1")

    total = sum( [ ((2*l*w) + (2*w*h) + (2*h*l) + min( l*w, l*h, w*h) ) for (l,w,h) in vals ] )
    print("Total: %s" % (total,))
    
if args.p2:
    print("Doing part 2")

    total = sum( [ ( min( 2*l+2*w, 2*w+2*h, 2*l+2*h) + l*w*h ) for (l,w,h) in vals ] )
    print("Total: %s" % (total,))
