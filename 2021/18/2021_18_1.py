#!/usr/bin/env python3

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

lineRe = re.compile("[\[\],\d]*")
data = []

def totuple(pair):
    if isinstance(pair,list):
        return tuple(( totuple(c) for c in pair ))
    else:
        return pair

    
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(totuple(eval(x)))


    
for d in data:
    print(f"Data: {d}")

    
def flatten(pair, output = None):
    if output == None:
        output = []
    if isinstance(pair, tuple):
        output.append("[")

        for e in pair:
            flatten(e,output)

        output.append("]")
    else:
        output.append(pair)

    return output

def topair(flat):
    output = []

    stack = [ output ]
    
    for c in flat:
        if c == '[':
            newval = []
            stack[-1].append(newval)
            stack.append( newval )
            
        elif c == ']':
            stack.pop()
        else:
            stack[-1].append(c)
    return totuple(output[0])

def explode(flat, ndx):
    for i in range(ndx-1,-1,-1):
        if isinstance(flat[i],int):
            flat[i] = flat[i] + flat[ndx]
            break
    for i in range(ndx+2,len(flat)):
        if isinstance(flat[i],int):
            flat[i] = flat[i] + flat[ndx+1]
            break
    flat[ndx-1:ndx+3] = [0]

def checkExplode(flat):
    depth = 0
    for i in range(0,len(flat)-2):
        if flat[i] == '[':
            depth = depth + 1
        elif flat[i] == ']':
            depth = depth - 1
        elif isinstance(flat[i],int) and isinstance(flat[i+1],int) and depth >= 5:
            #print(f"Explode {flat[i:i+2]} at depth {depth}")
            explode(flat, i)
            return True
    return False

def split(flat,i):
    n = flat[i]
    flat[i:i+1] = [ '[', n // 2, n - (n // 2), ']' ]

def checkSplit(flat):
    for i in range(0,len(flat)):
        if isinstance(flat[i],int) and flat[i] >= 10:
            #print(f"Split {flat[i]}")
            split(flat,i)
            return True
    return False

def reduce(pair):
    flat = flatten(pair)
    while True:
        #print(f"{flat}")
        if checkExplode(flat):
            continue
        if checkSplit(flat):
            continue
        return topair(flat)


def add(pair1, pair2):
    return reduce( (pair1,pair2) )

def magnitude(pair):
    if isinstance(pair,int):
        return pair
    else:
        return 3 * magnitude(pair[0]) + 2 * magnitude(pair[1])

if args.p1:
    print("Doing part 1")

    result = data[0]
    for d in data[1:]:
        result = add(result, d)

    print(f"Result: {result}")
    print(f"Magnitude: {magnitude(result)}")
    
    
if args.p2:
    print("Doing part 2")

    maxi = None
    maxj = None
    maxmag = None
    
    for i in range(0,len(data)):
        for j in range(0,len(data)):
            if i != j:
                result = add( data[i], data[j] )
                mag = magnitude(result)

                if maxmag == None or maxmag < mag:
                    maxi = i
                    maxj = j
                    maxmag = mag

    print(f"Largest Magnitude ({maxi},{maxj}): {maxmag}")
