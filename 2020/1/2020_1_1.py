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

data = []
lineRe = re.compile("\d+")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(int(x))

print("Data: %s" % (data,))
    
if args.p1:
    print("Doing part 1")

    for x,y in itertools.product(data,data):
        if x + y == 2020 :
            print("%s * %s = %s" % (x,y,x*y,))

            break
if args.p2:
    print("Doing part 2")

    for x,y,z in itertools.product(data,data,data):
        if x + y + z== 2020 :
            print("%s * %s * %s = %s" % (x,y,z,x*y*z,))

            break
