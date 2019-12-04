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

lineRe = re.compile("(\d+)-(\d+)")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    vals = (int(m.group(1)), int(m.group(2)), )

print("Vals: %s" % (vals,))

def valid(n):
    ns = "%s" % (n,)
    if len(ns) != 6:
        return False

    adjeq = False

    for i in range(0,len(ns)-1):
        if ns[i] > ns[i+1]:
            return False

    for a,b in zip(ns,ns[1:]):
        if a == b:
            adjeq = True

    if not adjeq:
        return False
        
    return True

if args.p1:
    print("Doing part 1")

    numvalid = 0
    for n in range(vals[0],vals[1]+1):
        if valid(n):
            #print("Valid: %s" % (n,))

            numvalid += 1

    print("Number valid: %s" % (numvalid,))
    
def valid2(n):
    ns = "%s" % (n,)
    if len(ns) != 6:
        return False

    adjeq = False

    for i in range(0,len(ns)-1):
        if ns[i] > ns[i+1]:
            return False

        if ns[i] == ns[i+1] and (i == 0 or ns[i] != ns[i-1]) and (i + 2 >= len(ns) or ns[i] != ns[i+2]):
            adjeq = True

    if not adjeq:
        return False
        
    return True

if args.p2:
    print("Doing part 2")
    
    numvalid = 0
    for n in range(vals[0],vals[1]+1):
        if valid2(n):
            #print("Valid: %s" % (n,))

            numvalid += 1

    print("Number valid: %s" % (numvalid,))
