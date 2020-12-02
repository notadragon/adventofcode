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

lineRe = re.compile("(\d+)-(\d+) ([a-z]): ([a-z]+).*")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( (int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)) )

if args.p1:
    print("Doing part 1")

    valid = 0
    for l,h,letter,pw in data:
        count = 0
        for c in pw:
            if c == letter:
                count = count + 1
        if count >= l and count <= h:
            print("%s-%s %s: %s" % (l,h,letter,pw,))
            valid = valid + 1
    print("Valid: %s" % (valid,))
            
    
    
if args.p2:
    print("Doing part 2")

    valid = 0
    for p1,p2,letter,pw in data:
        count = 0
        if (pw[p1-1] == letter) != (pw[p2-1] == letter):
            print("%s-%s %s: %s" % (p1,p2,letter,pw,))
            valid = valid + 1
    print("Valid: %s" % (valid,))
