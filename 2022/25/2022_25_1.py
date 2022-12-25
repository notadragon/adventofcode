#!/usr/bin/env pypy3

import argparse, re, itertools, collections

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')

args = parser.parse_args()

if not args.p1:
    args.p1 = True

print("Input: %s P1: %s" % (args.input,args.p1))

lineRe = re.compile("^[-=012]+$")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

dvals = {
    "2" : 2,
    "1" : 1,
    "0" : 0,
    "-" : -1,
    "=" : -2,
    }
vvals = { v:d for d,v in dvals.items() }
    
    
def convertSnafu(snafu):
    output = 0
    pow = 1
    for d in reversed(snafu):
        v = dvals[d]
        output = output + v * pow
        pow = pow * 5
    return output

def convertNum(num):
    if not num:
        return "0"
    
    snigits = []
    while num:
        m = num % 5
        if m > 2:
            m = m - 5
        snigits.append( vvals[m] )
        num = num - m
        num //= 5
    return "".join(reversed(snigits))
               

if args.p1:
    print("Doing part 1")

    total = 0
    for d in data:
        v = convertSnafu(d)
        d2 = convertNum(v)
        #if d != d2:
        #    print(f"{d} -> {v} -> {d2}")
        #else:
        #    print(f"{d} -> {v}")
        total = total + v
        
    print(f"Total: {total}")
    stotal = convertNum(total)
    print(f"SNAFU Total: {stotal}")
