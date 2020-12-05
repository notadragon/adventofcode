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

lineRe = re.compile("[FB]{7}[LR]{3}")
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

def makerowids(low,hi,bits):
    output = {}
    for i in range(0,1 << bits):
        
        binrep = "{0:b}".format(i)
        while len(binrep) < bits:
            binrep = "0" + binrep
        irep = "".join([ hi if b == "1" else low for b in binrep ])
        output[irep] = i
    return output

rowids = makerowids("F","B",7)
seatids = makerowids("L","R",3)
        
#print("%s: "  % (rowids,))


def seatid(seat):
    rownum = rowids[seat[0:7]]
    colnum = seatids[seat[7:10]]
    return rownum * 8 + colnum

if args.p1:
    print("Doing part 1")

#    for seat in data:
#        r = (0,127)
#        for x in seat[0:7]:
#            m = (r[0] + r[1]) / 2
#            if x == "F":
#                r = (r[0],m,)
#            else:
#                r = (m+1,r[1],)
#            print("%s" % (r,))
#        row = r[0]
#    for seat in data:
#        print("%s -> %s" % (seat,seatid(seat)))

    print("Max seatid: %s" % ( max([seatid(seat) for seat in data]),))
    
        
if args.p2:
    print("Doing part 2")

    seats = set([ seatid(seat) for seat in data])
    i = 1
    while True:
        if i in seats:
            i = i + 1
            continue
        if i-1 in seats and i+1 in seats:
            break
        i = i + 1

    print("My Seat: %s" % (i,))
    
    
