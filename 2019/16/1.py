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

lineRe = re.compile("\d+")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line

    inval = [ int(c) for c in x ]

print("Inval: %s" % (inval,))

def genpattern(p):
    while True:
        for i in range(0,p+1):
            yield 0
        for i in range(0,p+1):
            yield 1
        for i in range(0,p+1):
            yield 0
        for i in range(0,p+1):
            yield -1

def phase(inval,minoffset):
    s = len(inval) + minoffset
    #print("Total Length: %s + %s = %s" % (minoffset,len(inval),s,) )
    output = [0] * len(inval)

    i = minoffset
    while i < s:
        j = i
        oval = 0
        while j < s:
            for c in range(j, min(s,j + i + 1)):
                oval += inval[c-minoffset]
            j = j + (2 * i + 2)
            for c in range(j, min(s,j + i + 1)):
                oval -= inval[c-minoffset]
            j = j + (2 * i + 2)

        output[i-minoffset] = oval
        i = i + 1
        
        if i*2 > s:
            break

    while i < s:
        # everything in [i,s) is 1, at least one value computed
        output[i-minoffset] = output[i-1-minoffset] - inval[i-1-minoffset]
        i = i + 1

    for i in range(0,len(output)):
        output[i] = abs(output[i]) % 10
        
    return output
                
def phasex(inval,minoffset):
    output = []
    for i in range(0,len(inval)):
        pattern = genpattern(i)
        next(pattern)
        ival = 0
        #toprint = []
        for j in range(0,len(inval)):
            p = next(pattern)
            ival += p * inval[j]
            #toprint.append("%s*%s" % (inval[j],p,))
        newval = abs(ival) % 10
        output.append( newval )

        #print("%s = %s" % (" + ".join(toprint), newval,) )
    return output

if args.p1:
    print("Doing part 1")

    l = inval
    for i in range(0,100):
        l = phase(l,0)
    
    print("After 100 : %s" % (l,))
    print("First 8: %s" % ( "".join([ str(c) for c in l[0:8] ]), ))
    
if args.p2:
    print("Doing part 2")

    l = inval * 10000
    offset = int( "".join([ str(c) for c in inval[0:7] ]) )
    print("Offset: %s len: %s" % (offset,len(l),))

    l = l[offset:]
    for i in range(0,100):
        print("Step: %s" % (i,))
        l = phase(l,offset)
        
    l = ([0] * offset) + l

    print("l: %s" % (len(l),))
    
    print("Offset: %s" % (offset,))
    print("Signal: %s" % ( "".join( [str(c) for c in l[offset:offset+8] ]), ))
