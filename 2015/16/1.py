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

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("Sue ([0-9]+): (.*)")
statRe = re.compile("([a-z]+): ([0-9]+)")
realsue = {"children": 3,
           "cats": 7,
           "samoyeds": 2,
           "pomeranians": 3,
           "akitas": 0,
           "vizslas": 0,
           "goldfish": 5,
           "trees": 3,
           "cars": 2,
           "perfumes": 1, }

sues = {}
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    sueid = int(m.group(1))
    suedata = {}
    for f in statRe.findall(m.group(2)):
        suedata[f[0]] = int(f[1])
    sues[sueid] = suedata

if args.p1:
    print("Doing part 1")

    for sueid, suedata in sues.items():
        matches = True
        for item,num in suedata.items():
            if item in realsue:
                if num != realsue[item]:
                    matches = False
            else:
                if num != 0:
                    matches = False
        if matches:
            print("Real Sue: %s" % (sueid,))
        
if args.p2:
    print("Doing part 2")

    for sueid, suedata in sues.items():
        matches = True
        for item,num in suedata.items():
            if item in realsue:
                if item == "cats" or item == "trees":
                    if num <= realsue[item]:
                        matches = False
                elif item == "pomeranians" or item == "goldfish":
                    if num >= realsue[item]:
                        matches = False
                else:
                    if num != realsue[item]:
                        matches = False
            else:
                if num != 0:
                    matches = False
        if matches:
            print("Real Sue: %s" % (sueid,))
