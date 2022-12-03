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

lineRe = re.compile("([A-C]) ([X-Z])")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append( ( m.group(1), m.group(2), ) )

#for d in data:
#    print(f"{d}")
    
if args.p1:
    print("Doing part 1")

    def score(abc, xyz):
        aval = ord(abc) - ord("A")
        xval = ord(xyz) - ord("X")
        shapescore = xval + 1

        gamediff = (xval - aval) % 3
        if gamediff == 0:
            gamescore = 3
        elif gamediff == 1:
            gamescore = 6
        else:
            gamescore = 0

        return shapescore + gamescore

    #for d in data:
    #    print(f"{d} -> {score(d[0], d[1])}")
            
    total = sum( [ score(d[0], d[1]) for d in data ])
    print(f"{total}")
    
if args.p2:
    print("Doing part 2")

    def score(abc, xyz):
        aval = ord(abc) - ord("A")

        if "X" == xyz:
            xval = (aval - 1) % 3
        elif "Y" == xyz:
            xval = aval
        else:
            xval = (aval + 1) % 3
            
        shapescore = xval + 1

        gamediff = (xval - aval) % 3
        if gamediff == 0:
            gamescore = 3
        elif gamediff == 1:
            gamescore = 6
        else:
            gamescore = 0

        return shapescore + gamescore        

    total = sum( [ score(d[0], d[1]) for d in data ])
    print(f"{total}")
