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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

lineRe = re.compile("(toggle|turn off|turn on) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)")
actions = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    m = lineRe.match(x)
    if not m:
        print ("Invalid line: %s" % (x,))
        continue

    actions.append( (m.group(1), (int(m.group(2)),int(m.group(3)),), (int(m.group(4)),int(m.group(5)),),) )

#print("Actions: %s" % (actions,))

if args.p1:
    print("Doing part 1")

    lights = []
    for i in range(0,1000):
        lightsline = []
        for j in range(0,1000):
            lightsline.append(False)
        lights.append(lightsline)

    for action,fromloc,toloc in actions:
        for i in range(fromloc[0],toloc[0]+1):
            for j in range(fromloc[1],toloc[1]+1):
                if action == "toggle":
                    lights[i][j] = not lights[i][j]
                elif action == "turn on":
                    lights[i][j] = True
                elif action == "turn off":
                    lights[i][j] = False


    total = 0
    for i in range(0,1000):
        for j in range(0,1000):
            if lights[i][j]:
                total += 1
    print("Total on: %s" % (total,))
    
if args.p2:
    print("Doing part 2")
    lights = []
    for i in range(0,1000):
        lightsline = []
        for j in range(0,1000):
            lightsline.append(0)
        lights.append(lightsline)

    for action,fromloc,toloc in actions:
        for i in range(fromloc[0],toloc[0]+1):
            for j in range(fromloc[1],toloc[1]+1):
                if action == "toggle":
                    lights[i][j] = lights[i][j] + 2
                elif action == "turn on":
                    lights[i][j] = lights[i][j] + 1
                elif action == "turn off":
                    lights[i][j] = max(0,lights[i][j]-1)


    total = 0
    for i in range(0,1000):
        for j in range(0,1000):
            total += lights[i][j]
    print("Total on: %s" % (total,))
    
