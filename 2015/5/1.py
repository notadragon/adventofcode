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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

ivals = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    ivals.append(x)

#print("Ivals: %s" % (ivals,))

def isnice(x):
    vowels = 0
    hasdouble = False
    naughty = False
    
    prevc = " "
    for c in x:
        if c in "aeiou":
            vowels = vowels + 1
        if c == prevc:
            hasdouble = True

        if prevc == "a" and c == "b":
            naughty = True
        if prevc == "c" and c == "d":
            naughty = True
        if prevc == "p" and c == "q":
            naughty = True
        if prevc == "x" and c == "y":
            naughty = True
            
        prevc =c
    return vowels >= 3 and hasdouble and (not naughty)

if args.p1:
    print("Doing part 1")

    nicetotal = 0
    for x in ivals:
        nice = isnice(x)
        if nice:
            nicetotal += 1
        #print("%s -> %s" % (x,nice,))
    print("%s nice / %s" % (nicetotal, len(ivals),))

nice2Re1 = re.compile(".*(..).*\\1.*")
nice2Re2 = re.compile(".*(.).\\1.*")
def isnice2(x):
    if not nice2Re1.match(x):
        return False
    if not nice2Re2.match(x):
        return False
    return True
    
if args.p2:
    print("Doing part 2")

    nicetotal = 0
    for x in ivals:
        nice = isnice2(x)
        if nice:
            nicetotal += 1
        #print("%s -> %s" % (x,nice,))
    print("%s nice / %s" % (nicetotal, len(ivals),))
