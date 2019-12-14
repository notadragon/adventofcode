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

lineRe = re.compile("((?:\d+ [A-Z]+)(?:, \d+ [A-Z]+)*) => (\d+ [A-Z]+)")

reactions = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))

    def parsevalue(c):
        c = c.strip().split(" ")
        return ( int(c[0]), c[1], )

    # Process input line
    inputs = tuple([ parsevalue(c) for c in m.group(1).split(",")])
    output = parsevalue(m.group(2))
    reactions.append( (inputs, output,) )

for r in reactions:
    print("%s" % (r,))

def neededOre(numneeded):
    wanted = { "FUEL" : numneeded }
    reversals = { r[1][1] : r  for r in reactions }

    products = set( [ r[1][1] for r in reactions ] )
    
    levels = { "ORE":0 }
    toprocess = reactions[:]
    while toprocess:
        newtoprocess = []
        for r in toprocess:
            rlevel = 0
            for i in r[0]:
                if i[1] not in levels:
                    rlevel = None
                    break
                else:
                    rlevel = max(rlevel,levels[i[1]])
            #print("%s -> %s:%s" % (r,r[1][1],rlevel))
            if rlevel != None:
                levels[r[1][1]] = rlevel + 1
            else:
                newtoprocess.append(r)
        #print("Levels: %s" % (levels,))
        toprocess = newtoprocess

    #print("Levels: %s" % (levels,))
                    
    while "ORE" not in wanted or len(wanted) > 1:
        #print("Wanted: %s" % (wanted,))

        pl = -1
        toproduce = None
        for p in wanted.keys():
            if not toproduce or levels[p] > pl:
                toproduce = p
                pl = levels[p]

        #print("Producing: %s: %s" % (pl,toproduce,))

        num = wanted[toproduce]
        del wanted[toproduce]

        r = reversals[toproduce]
        rnum = num // r[1][0] + (num % r[1][0] > 0)

        for input in r[0]:
            wanted[input[1]] = wanted.get(input[1],0) + input[0] * rnum

    return wanted["ORE"]
            
if args.p1:
    print("Doing part 1")

    print("Wanted: %s" % (neededOre(1),))

if args.p2:
    print("Doing part 2")

    target = 1000000000000

    maxFuel = 1
    maxNeeded = neededOre(maxFuel)
    oneNeeded = maxNeeded
    
    while True:
        print("Fuel: %s Ore: %s" % (maxFuel,maxNeeded,))

        extra = target - maxNeeded
        guess = maxFuel + max(extra // oneNeeded,1)

        guessNeeded = neededOre(guess)
        if guessNeeded < target:
            maxFuel = guess
            maxNeeded = guessNeeded
        else:
            break

        
