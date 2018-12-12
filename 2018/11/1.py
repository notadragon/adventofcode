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

lineRe = re.compile(".*")


for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    serialNum = int(x)

print("Serial#:%s" % (x,))

powers = {}

def retrieve(x,y,w):
    pw = powers.get(w,None)
    if pw:
        return pw[x-1][y-1]
    else:
        return None


def store(x,y,w,p):
    pw = powers.setdefault(w,None)
    if not pw:
        pw = [None] * 300
        for i in range(0,300):
            pw[i] = [None] * 300
        powers[w] = pw
    pw[x-1][y-1] = p
    
def power(x,y):
    p = retrieve(x,y,1)
    if p != None:
        return p
    
    rackId = x+10
    p = rackId * y
    p += serialNum
    p = p * rackId
    p = (p/100) % 10
    p = p - 5

    store(x,y,1,p)
    return p

def gridpower(x,y,w,h):
    if w != h:
        m = min(w,h)
        output = power(x,y,m,m)
        if w == m:
            output += gridpower(x,y+m,w,h-m)
        else:
            output += gridpower(x+m,y,w-m,h)
        return output

    output = retrieve(x,y,w)
    if output != None:
        return output

    if w == 1:
        output = power(x,y)
    elif w == 2:
        output = power(x,y) + power(x+1,y) + power(x,y+1) + power(x+1,y+1)
    else:
        output = gridpower(x,y,w-1,h-1) + gridpower(x+1,y+1,w-1,h-1) + gridpower(x+w-1,y,1,1) + gridpower(x,y+h-1,1,1) - gridpower(x+1,y+1,w-2,h-2)

    store(x,y,w,output)
    return output

def printGrid(x,y,wx,wy):
    lines = []
    for yv in range(y,y+wy):
        line = []
        for xv in range(x,x+wx):
            line.append("%4d" % (power(xv,yv),))
        lines.append("".join(line))
    return lines

def showGrid(x,y,wx,wy):
    for l in printGrid(x,y,wx,wy):
        print(l)

if args.p1:
    print("Doing part 1")

    maxpower = 0
    maxlocs = set()
    maxloc = None
    for y in range(1,297+1):
        for x in range(1,297+1):
            p = gridpower(x,y,3,3)
            if p == maxpower:
                maxlocs.add( (x,y,) )
            elif p > maxpower:
                maxlocs = set()
                maxlocs.add( (x,y,) )
                maxloc = (x,y,)
                maxpower = p
    print("Max power: %s Max loc: %s,%s" % (maxpower,maxloc[0],maxloc[1],))
    showGrid(maxloc[0]-1,maxloc[1]-1,5,5)
            
if args.p2:
    print("Doing part 2")
    
    maxpower = 0
    maxlocs = set()
    maxloc = None
    for w in range(1,300):
        if w > 4:
            del powers[w-3]
        #print("W:%s" % (w,))
        for y in range(1,301 - w):
            for x in range(1,301 - w):
                p = gridpower(x,y,w,w)
                if p == maxpower:
                    maxlocs.add( (x,y,w,) )
                elif p > maxpower:
                    maxlocs = set()
                    maxlocs.add( (x,y,w,) )
                    maxloc = (x,y,w,)
                    maxpower = p
                    #print("Max update: %s = %s" % (maxloc,maxpower,))
    showGrid(maxloc[0]-1,maxloc[1]-1,maxloc[2]+2,maxloc[2]+2)
    print("Max Power: %s Max loc: %s,%s,%s" % (maxpower,maxloc[0],maxloc[1],maxloc[2]))
    
