#!/usr/bin/env pypy3

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

lineRe = re.compile("^.*$")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( tuple( int(y) for y in x.split(" ") ) )

for d in data:
    print(f"{d}")

def iszeros(sequence):
    for i in sequence:
        if i != 0:
            return False
    return True

def deriv(sequence):
    return tuple( y - x for x,y in zip( sequence[0:-1], sequence[1:] ) )
    
def predict(sequence):
    if iszeros(sequence):
        return 0

    d = deriv(sequence)
    nextderiv = predict(d)

    return sequence[-1] + nextderiv

def prevpredict(sequence):
    if iszeros(sequence):
        return 0
    d = deriv(sequence)
    prevderiv = prevpredict(d)
    return sequence[0] - prevderiv

if args.p1:
    print("Doing part 1")

    total = 0
    for d in data:
        p = predict(d)
        print(f"{d} -> {p}")
        total = total + p
    print(f"Total: {total}")
    
if args.p2:
    print("Doing part 2")

    total = 0
    for d in data:
        p = prevpredict(d)
        print(f"{d} -> {p}")
        total = total + p
    print(f"Total: {total}")
