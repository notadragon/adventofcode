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

    # Process input line
    ival = x

print("Ival:%s" % (ival,))

def increment(p):

    numzs = 0
    while numzs < len(p) and p[-1 - numzs] == "z":
        numzs = numzs + 1
    top = len(p) - numzs - 1

    cchar = chr(ord(p[top])+1)
    if cchar == "i" or cchar == "o" or cchar == "l":
        cchar= chr(ord(cchar)+1)
    
    return p[0:top] + cchar + "a" * numzs

re1 = re.compile(".*(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz).*")
re3 = re.compile(".*(.)\\1.*(.)\\2.*")

def isvalid(p):
    if "i" in p or "o" in p or "l" in p:
        return False
    if not re1.match(p):
        return False
    if not re3.match(p):
        return False
    return True

x = ival
while True:
    x = increment(x)
    if isvalid(x):
        print("Next valid:%s" % (x,))
        p1val = x
        break
    #print("Not Valid: %s" % (x,))

x = p1val
while True:
    x = increment(x)
    if isvalid(x):
        print("Next valid:%s" % (x,))
        p2val = x
        break
    
if args.p1:
    print("Doing part 1")

    print("P1Val:%s" % (p1val,))


        
if args.p2:
    print("Doing part 2")

    print("P2Val:%s" % (p2val,))
