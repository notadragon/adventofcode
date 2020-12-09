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

lineRe = re.compile("\d+")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(int(x))

#for d in data:
#    print("%s"% (d,))

if args.p1:
    print("Doing part 1")

    def isSumOfPair(x,r):
        for i in range(0,len(r)):
            for j in range(i+1,len(r)):
                if r[i] + r[j] == x:
                    return True
        return False

    rsize = 25
    for i in range(rsize,len(data)):
        x = data[i]
        if not isSumOfPair(x,data[i-rsize:i]):
            invalidNum = x
            print("Invalid: %s" % (x,))
            break
    
if args.p2:
    print("Doing part 2")

    for i in range(0,len(data)):
        x = 0
        for j in range(i,len(data)):
            x += data[j]
            if x == invalidNum and j > i:
                minval = min(data[i:j+1])
                maxval = max(data[i:j+1])
                print("sum(%s,%s) = %s (weakness: %s + %s = %s)" % (i,j,x,minval,maxval,minval+maxval,))
            if x >= invalidNum:
                break

            
        
