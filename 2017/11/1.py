#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)


def gethash(listsize,lengths,repeats):
    numbers = list(range(0,listsize))
    currentpos = 0 # rotating list so this is always 0
    skipsize = 0
    skipped = 0
    for i in range(0,repeats):
      for length in lengths:
        numbers = list(reversed(numbers[0:length])) + numbers[length:]

        toskip = (length + skipsize) % len(numbers)

        numbers = numbers[toskip:] + numbers[:toskip]

        skipped += toskip
        skipsize = skipsize + 1
    toskip = len(numbers) - (skipped % len(numbers))
    numbers = numbers[toskip:] + numbers[:toskip]
    return numbers

if args.p1:
    print "Doing part 1"

    lines = open(args.input).readlines()
    listsize = int(lines[0])
    inputs = [int(x) for x in lines[1].split(",")]
    
    print "inputs:%s" % (inputs,)

    numbers = gethash(listsize,inputs,1)
    print "hash: %s" % (numbers,)
    print " n[0] * n[1]: %s" % (numbers[0]*numbers[1],)
    
if args.p2:
    print "Doing part 2"

    lines = open(args.input).readlines()
    listsize = int(lines[0])
    inputs = [ord(x) for x in lines[1].strip()]

    inputs += [17,31,73,47,23]

    print "inputs:%s" % (inputs,)

    sparsehash = gethash(listsize,inputs,64)
    print "sparsehash:%s" % (sparsehash,)

    densehash = []
    for i in range(0,256,16):
        toxor = sparsehash[i:i+16]
        xor = 0
        for h in toxor:
            xor = xor ^ h
        densehash.append(xor)

    print "densehash:%s" % (densehash,)

    rep = "".join(["%02x" % x for x in densehash])
    print "rep: %s" % (rep,)
    
