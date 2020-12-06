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

lineRe = re.compile("[a-z]*")
data = []

for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

def getanswers(data):
    out = []
    for d in data:
        if d:
            out.append(d)
        else:
            yield out
            out = []
    if out:
        yield out

#for ga in getanswers(data):
#    print("%s" % (ga,))
        
if args.p1:
    print("Doing part 1")

    totalanswered = 0
    for ga in getanswers(data):
        gas = set()
        for pa in ga:
            for a in pa:
                gas.add(a)
        totalanswered += len(gas)
    print("Total Answered: %s" % (totalanswered,))
    
if args.p2:
    print("Doing part 2")

    totalanswered = 0
    for ga in getanswers(data):
        gas = set()
        for pa in ga:
            for a in pa:
                gas.add(a)
        gaas = set()
        for a in gas:
            answered = True
            for pa in ga:
                if a not in pa:
                    answered = False
            if answered:
                gaas.add(a)
        totalanswered += len(gaas)
    print("Total Answered: %s" % (totalanswered,))
