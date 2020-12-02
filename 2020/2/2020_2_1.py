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

def countvalid(d,f):
    return len([t for t in d if f(t)])

if args.p1:
    print("Doing part 1")

    def isvalid(t):
        l,h,letter,pw =t
        c = len([x for x in pw if x == letter])
        return c >= l and c <= h
    
    
    valid = countvalid(data,isvalid)
    print("Valid: %s" % (valid,))
            
    
    
if args.p2:
    print("Doing part 2")

    def isvalid(t):
        p1,p2,letter,pw =t
        return (pw[p1-1] == letter) != (pw[p2-1] == letter)
    
    valid = countvalid(data,isvalid)
    print("Valid: %s" % (valid,))
