#!/usr/bin/env python3

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

lineRe = re.compile("([a-z]+(?: [a-z]+)*) \| ([a-z]+(?: [a-z]+)*)")

data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    k1 = m.group(1).split(" ")
    k2 = m.group(2).split(" ")
    data.append( (k1,k2) )

#for d in data:
#    print(f"{d}")

digits = {
    0 : "abcefg",
    1 : "cf",
    2 : "acdeg",
    3 : "acdfg",
    4 : "bcdf",
    5 : "abdfg",
    6 : "abdefg",
    7 : "acf",
    8 : "abcdefg",
    9 : "abcdfg",
    }

signalCounts = [0] * 7
for v in digits.values():
    for c in v:
        ndx = ord(c) - ord("a")
        signalCounts[ndx] = signalCounts[ndx] + 1

countMapping = {}
for k,v in digits.items():
    vcounts = tuple(sorted([ signalCounts[ord(c)-ord("a")] for c in v ]))
    countMapping[vcounts] = k
    print(f"{k} - {v} - {vcounts}")


def getMapping(dispdigits):
    dispCounts = [0] * 7

    for v in dispdigits:
        for c in v:
            ndx = ord(c) - ord("a")
            dispCounts[ndx] = dispCounts[ndx] + 1

    out = {}

    for v in dispdigits:
        dcounts = tuple(sorted([ dispCounts[ord(c)-ord("a")] for c in v ]))
        digit = countMapping[dcounts]
        sortedv = "".join(sorted(v))
        out[sortedv] = digit

    return out
        
if args.p1:
    print("Doing part 1")

    counts = [0] * 10
    for dd, display in data:
        #print(f"{display}")
        for dval in display:
            #print(dval)
            for realdigit,realdisp in digits.items():
                if len(realdisp) == len(dval):
                    
                    counts[realdigit] = counts[realdigit] + 1
                    #if realdigit == 1 or realdigit == 4 or realdigit == 7 or realdigit == 8:
                    #    print(f" {dval} -> {realdigit}")

    print(f"Possible Counts: {counts}")
    print(f"1+4+7+8: {counts[1] + counts[4] + counts[7] + counts[8]}")
        
if args.p2:
    print("Doing part 2")

    total = 0
    for digits,display in data:
        mapping = getMapping(digits)

        print(f"Digits: {digits}")
        print(f"Mapping: {mapping}")

        sorteddisplay = [ "".join(sorted(d)) for d in display ]
        
        shown = [ str(mapping[d]) for d in sorteddisplay ]

        val = int("".join(shown))
        
        print(f"Display: {display} -> {shown} = {val}")
        total += val

    print(f"Total: {total}")
    
