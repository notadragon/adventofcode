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

lineRe = re.compile("position=< *(-?[0-9]+), *(-?[0-9]+)> velocity=< *(-?[0-9]+), *(-?[0-9]+)>")
lights = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    lights.append( ( (int(m.group(1)),int(m.group(2)),), (int(m.group(3)),int(m.group(4)),), ) )

#print("Lights; %s" % (lights,))

class Lights:
    def __init__(self,lights):
        self.lights = tuple(lights)
        self.minx = min([ l[0][0] for l in self.lights ])
        self.maxx = max([ l[0][0] for l in self.lights ])
        self.miny = min([ l[0][1] for l in self.lights ])
        self.maxy = max([ l[0][1] for l in self.lights ])

    def iterate(self):
        return Lights( [ ( (l[0][0] + l[1][0], l[0][1] + l[1][1]), l[1] ) for l in self.lights ] )

    def show(self):
        for y in range(self.miny,self.maxy+1):
            row = ["."] * (self.maxx - self.minx + 1)
            for l in self.lights:
                if l[0][1] == y:
                    row[l[0][0] - self.minx] = "#"
            print "".join(row)
    
if args.p1:
    print("Doing part 1")

    l = Lights(lights)

    height = l.maxy - l.miny
    second = 0
    while True:
        nextl = l.iterate();
        nextsecond = second + 1
        nextheight = nextl.maxy - nextl.miny

        if nextheight > height:
            print("Second:%s" % (second,))
            l.show()
            break

        l = nextl
        second = nextsecond
        height = nextheight
        
if args.p2:
    print("Doing part 2")
