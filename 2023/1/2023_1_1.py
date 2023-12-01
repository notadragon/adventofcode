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

values = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    values.append(x)

#for x in values:
#    print(x)

if args.p1:
    print("Doing part 1")

    total = 0
    for x in values:
        digits = [ c for c in x if c.isdigit() ]
        val = int(digits[0]) * 10 + int(digits[-1])

        print(f"{x} -> {digits} -> {val}")
        
        total = total + val

    print(f"total: {total}")


if args.p2:
    print("Doing part 2")

    digitsre = re.compile("[0-9]|one|two|three|four|five|six|seven|eight|nine")

    digitsmap = {
        "one" : 1,
        "two" : 2,
        "three" : 3,
        "four" : 4,
        "five" : 5,
        "six" : 6,
        "seven" : 7,
        "eight" : 8,
        "nine" : 9,
        }
    for i in range(0,10):
        digitsmap[ str(i) ] = i

    print(f"DigitsMap: {digitsmap}")

    def findfirst(x):
        for i in range(0,len(x)):
            rem = x[i:]
            for k in digitsmap.keys():
                if rem.startswith(k):
                    return digitsmap[k]

    def findlast(x):
        for i in range(len(x)-1,-1,-1):
            rem = x[i:]
            for k in digitsmap.keys():
                if rem.startswith(k):
                    return digitsmap[k]

    total = 0
    for x in values:
        digits = ( findfirst(x), findlast(x) )
        print(f"{x} -> {digits}")

        val = digits[0] * 10 + digits[1]
        total = total + val

    print(f"Total: {total}")
        
