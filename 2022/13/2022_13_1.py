#!/usr/bin/env pypy3

import argparse, re, itertools, collections, functools

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

lineRe = re.compile("^[\[\]0-9,]+$")

data = []
currData = None

def tupleify(d):
    if isinstance(d,list):
        return tuple(( tupleify(x) for x in d ))
    else:
        return d

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        currData = None
        continue
    
    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if currData == None:
        currData = []
        data.append(currData)
    currData.append(eval(x))
data = tupleify(data)

#for d in data:
#    print(f"Data: {d}")


def nextprefix(prefix):
    if prefix != None:
        return f"{prefix}  "
    else:
        return prefix

def doCompare(lhs, rhs, prefix=None):
    if prefix != None:
        print(f"{prefix}- Compare {lhs} vs {rhs}")
    if isinstance(lhs,int) and isinstance(rhs,int):
        if lhs < rhs:
            if prefix != None:
                print(f"{prefix}  - Left side is smaller, so inputs are *in the right order*")
            return -1
        elif lhs > rhs:
            if prefix:
                print(f"{prefix}  - Right side is smaller, so inputs are *not* in the right order")
            return 1
        return 0

    if isinstance(lhs,tuple) and isinstance(rhs,tuple):
        lhslen = len(lhs)
        rhslen = len(rhs)

        for i in range(0,min(lhslen,rhslen)):
            c = doCompare(lhs[i],rhs[i],nextprefix(prefix))
            if c != 0:
                return c
        if lhslen < rhslen:
            if prefix != None:
                print(f"{prefix}  - Left side ran out of items, so inputs are *in the right order*")
            return -1
        elif lhslen > rhslen:
            if prefix != None:
                print(f"{prefix}  - Right side ran out of items, so inputs are *not* in the right order")
            return 1
        else:
            return 0

    if isinstance(lhs,int):
        newlhs = (lhs,)
        if prefix != None:
            print(f"{prefix}  - Mixed types; convert left to {newlhs} and retry comparison")
        return doCompare( newlhs, rhs, nextprefix(prefix))
    elif isinstance(rhs,int):
        newrhs = (rhs,)
        if prefix != None:
            print(f"{prefix}  - Mixed types; convert right to {newrhs} and retry comparison")
        return doCompare( lhs, newrhs, nextprefix(prefix))

if args.p1:
    print("Doing part 1")

    total = 0
    prefix = None
    
    for n,pair in enumerate(data,1):
        if prefix != None:
            print(f"== Pair {n} ==")
        left,right = pair

        comp = doCompare(left,right,prefix)

        if prefix != None:
            print(f"comp: {comp}")

        if comp < 0:
            total = total + n

    print(f"Right Indices Total: {total}")
        
    
    
if args.p2:
    print("Doing part 2")

    tosort = []
    for pair in data:
        left,right = pair
        tosort.append(left)
        tosort.append(right)

    dividers = [
        tupleify(eval("[[2]]")),
        tupleify(eval("[[6]]")),
        ]

    tosort.extend(dividers)

    tosort.sort(key=functools.cmp_to_key(doCompare))

    dividerindices = [None, None]
    for n,packet in enumerate(tosort,1):
        #print(f"{n} -> {packet}")
        for i in range(0,len(dividers)):
            if packet == dividers[i]:
                dividerindices[i] = n

    decoderkey = 1
    for ndx in dividerindices:
        decoderkey *= ndx
        
    #print(f"Divider Indices: {dividerindices}")
    print(f"Decoder Key: {decoderkey}")
