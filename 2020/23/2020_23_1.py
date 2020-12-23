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

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    labeling = x

print("Labeling: %s" % (labeling,))

def dostep(current,nextmap,valrange):
    """
    Perform one step, with the current cup being 'current', nextmap 
    containing the ccup id right of each cup, and valrange having 
    the [min,max] cup values
    """
    pickup = []
    for i in range(0,3):
        if pickup:
            pickup.append(nextmap[pickup[-1]])
        else:
            pickup.append(nextmap[current])

    destination = current - 1
    if destination < valrange[0]:
        destination = valrange[1]
    while destination in pickup or destination not in nextmap:
        destination = destination - 1
        if destination < valrange[0]:
            destination = valrange[1]

    nextmap[current] = nextmap[pickup[-1]]
    nextmap[pickup[-1]] = nextmap[destination]
    nextmap[destination] = pickup[0]

def solve(startorder,maxsize,steps):
    """
    Given an initial sequence ofc cups 'startorder', and total number of
    cups 'maxsize', perform 'steps' steps.  Return the new set of cups as
    an array    
    """
    
    nextmap = {}
    maxval = max(startorder)
    minval = min(startorder)

    # fill in the initial set of links
    for i in range(0,len(startorder)-1):
        nextmap[startorder[i]] = startorder[i+1]

    # fill in extra values after the initial list
    lastval = startorder[-1]
    nextval = maxval + 1
    while len(nextmap) < maxsize - 1:
        maxval = max(maxval,lastval)
        nextmap[lastval] = nextval
        lastval = nextval
        nextval = nextval + 1

    #link the last element back to the first element
    nextmap[lastval] = startorder[0]
    maxval = max(maxval,lastval)

    # iterate the right number of steps
    current = startorder[0]
    for i in range(0,steps):
        dostep(current,nextmap,(minval,maxval))
        current = nextmap[current]

    # build and return the final list of cups starting at cup #1
    output = [0] * len(nextmap)
    nextval = 1
    for i in range(0,len(output)):
        output[i] = nextval
        nextval = nextmap[nextval]

    return output
    
    
if args.p1:
    print("Doing part 1")

    cups = [ int(l) for l in labeling]
    lastcups = solve(cups, len(cups), 100)

    print("Final order 1 + %s" % ("".join([str(c) for c in lastcups[1:]]),))

        
if args.p2:
    print("Doing part 2")

    cups = [ int(l) for l in labeling]
    lastcups = solve(cups, 1000000, 10000000)

    print("Final order %s ... %s" % (", ".join([str(c) for c in lastcups[0:20]]),
                                         ", ".join([str(c) for c in lastcups[-20:]]),))
    print("Product: %s * %s = %s" % (lastcups[1],lastcups[2],lastcups[1]*lastcups[2],))
