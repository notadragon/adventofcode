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

lineRe = re.compile("^(?:([\.#]+)|)$")

maps = []

currmap = None
for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if x:
        if not currmap:
            currmap = []
        currmap.append(tuple( c for c in x) )
    else:
        maps.append(tuple(currmap) )
        currmap = None
if currmap:
    maps.append(tuple(currmap))
    currmap = None

#for m in maps:
#    print(f"Map: {m}")

def isvrefl(m, c):
    # c columns to the left of reflection
    for i in range(0,c):
        left = c - i - 1
        if left < 0:
            break
        right = c + i
        if right >= len(m[0]):
            break
        for y in range(0,len(m)):
            if m[y][left] != m[y][right]:
                return False
    return True

def iscrefl(m, c):
    # c rows above the reflection

    for i in range(0,c):
        top = c - i - 1
        if top < 0:
            break
        bottom = c + i
        if bottom >= len(m):
            break
        if m[top] != m[bottom]:
            return False
    return True

def refllines(m):
    output = []
    
    for x in range(1,len(m[0])):
        if isvrefl(m,x):
            #print(f"Reflect beteween columns {x}/{x+1}")
            output.append( ("v",x) )

    for y in range(1,len(m)):
        if iscrefl(m,y):
            #print(f"Reflect between rows {y}/{y+1}")
            output.append( ("h",y) )

    return output
    

if args.p1:
    print("Doing part 1")


    total = 0
    for m in maps:
        #print(f"Map: {m}")

        lines = refllines(m)

        #print(f"Map: {m}  Refls: {lines}")

        for t,c in lines:
            if t == "v":
                total = total + c
            elif t == "h":
                total = total + 100 * c

    print(f"Total: {total}")

def smudge(m,sx,sy):
    output = []
    for y in range(0,len(m)):
        r = m[y]
        if y == sy:
            newr = []

            for x in range(0,len(r)):
                if x == sx:
                    if r[x] == ".":
                        newr.append("#")
                    else:
                        newr.append(".")
                else:
                    newr.append(r[x])

            output.append(tuple(newr))
        else:
            output.append(r)
    return tuple(output)

    
if args.p2:
    print("Doing part 2")

    total = 0
    for m in maps:
        lines = refllines(m)
        #print(f"Map: {m}")
        #print(f"Lines: {lines}")
        added = set()
        for y in range(0,len(m)):
            for x in range(0,len(m[y])):
                sm = smudge(m,x,y)
                smlines = refllines(sm)

                newlines = 0
                for l in smlines:
                    if l not in lines:
                        newlines = newlines + 1
                        added.add(l)
                if newlines >= 1:
                    #print(f"Smudge ({x},{y}) -> {smlines}")
                    pass
        added = tuple(added)
        #print(f"Added reflections: {added}")

        for t,c in added:
            if t == "v":
                total = total + c
            elif t == "h":
                total = total + 100 * c

    print(f"Total: {total}")            
