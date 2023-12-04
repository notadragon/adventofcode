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

lineRe = re.compile("^Game ([0-9]+): (.*)$")
cubeRe = re.compile("([0-9]+) (red|green|blue)")

games = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    gamid = int(m.group(1))

    hands = m.group(2).split(";")
    handsdata = []
    for hand in hands:
        handdata = []
        for cubes in hand.split(","):
            cubem = cubeRe.match(cubes.strip())
            if not cubem:
                print("Invalid cubes?")

            handdata.append( (int(cubem.group(1)), cubem.group(2),) )
        handsdata.append(tuple(handdata))
    games.append( (gamid, tuple(handsdata), ) )

#for g in games:
#    print(f"{g}")
    
if args.p1:
    print("Doing part 1")

    total = 0
    
    for gamedata in games:

        mincubes = { "red": 0, "green" : 0, "blue" : 0 }

        for hand in gamedata[1]:
            for cubes in hand:
                mincubes[ cubes[1] ] = max(mincubes[ cubes[1] ], cubes[0] )

        if mincubes["red"] <= 12 and mincubes["green"] <= 13 and mincubes["blue"] <= 14:
            total = total + gamedata[0]

    print(f"Total: {total}")

    
if args.p2:
    print("Doing part 2")

    total = 0
    for gamedata in games:

        mincubes = { "red": 0, "green" : 0, "blue" : 0 }

        for hand in gamedata[1]:
            for cubes in hand:
                mincubes[ cubes[1] ] = max(mincubes[ cubes[1] ], cubes[0] )

        power = mincubes["red"] * mincubes["green"] * mincubes["blue"]

        total = total + power

    print(f"{total}")
