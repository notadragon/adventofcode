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

lineRe = re.compile(".*")
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



def get(data,x,y):
    if y < 0 or y >= len(data):
        return " "
    row = data[y]
    if x < 0 or x >= len(row):
        return ""
    return row[x]

deltas = [ d for d in itertools.product(range(-1,2),range(-1,2)) if d[0] != 0 or d[1] != 0 ]

def adjacents(data,x,y):
    for d in deltas:
        yield get(data,x+d[0],y+d[1])

def visibleadjacents(data,x,y):
    for d in deltas:
        offset = 1
        seen = get(data,x + offset*d[0], y + offset*d[1])
        while seen == ".":
            offset = offset + 1
            seen = get(data,x + offset*d[0], y + offset*d[1])
        yield seen

#for x in data:
#    print(x)

def nextData1(data):
    output = []
    for y in range(0,len(data)):
        inrow = data[y]
        outrow = []
        for x in range(0,len(inrow)):
            inval = get(data,x,y)
            adj = [ x for x in adjacents(data,x,y) ]
            
            outval = inval
            if inval == "L":
                if "#" not in adj:
                    outval = "#"
            elif inval == "#":
                adjocc = len([ x for x in adj if x == "#" ] )
                if adjocc >= 4:
                    outval = "L"
            outrow.append(outval)
        output.append("".join(outrow))
    return output

if args.p1:
    print("Doing part 1")

    lastdata = data
    ndata = nextData1(lastdata)
    while ndata != lastdata:
        lastdata = ndata
        ndata = nextData1(ndata)

    #for x in ndata:
    #    print(x)
    occupied = sum( [len([ x for x in r if x == "#"]) for r in ndata] )
    print("Occupied: %s" % (occupied,))


def nextData2(data):
    output = []
    for y in range(0,len(data)):
        inrow = data[y]
        outrow = []
        for x in range(0,len(inrow)):
            inval = get(data,x,y)
            adj = [ x for x in visibleadjacents(data,x,y) ]
            
            outval = inval
            if inval == "L":
                if "#" not in adj:
                    outval = "#"
            elif inval == "#":
                adjocc = len([ x for x in adj if x == "#" ] )
                if adjocc >= 5:
                    outval = "L"
            outrow.append(outval)
        output.append("".join(outrow))
    return output


if args.p2:
    print("Doing part 2")

    lastdata = data
    ndata = nextData2(lastdata)
    while ndata != lastdata:
        lastdata = ndata
        ndata = nextData2(ndata)

    #for x in ndata:
    #    print(x)
    occupied = sum( [len([ x for x in r if x == "#"]) for r in ndata] )
    print("Occupied: %s" % (occupied,))
