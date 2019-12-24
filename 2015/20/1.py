#!/usr/bin/env pypy

import argparse, re, itertools, collections, heapq

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
    target = int(x)

print("Target: %s" % (target,))

def numpresents(n):
    output = 0

    for i in range(1,n+1):
        if n % i == 0:
            output = output + 10 * i

    #print("%s: %s" % ( n, output, ) )
    return output

def sieve():
    yield 2
    yield 3
    yield 5
    yield 7
    sieve = []
    heapq.heappush(sieve, (15,3) )
    heapq.heappush(sieve, (15,5) )
    heapq.heappush(sieve, (21,7) )
    
    n = 11

    while True:
        if sieve[0][0] > n:
            yield n
        else:
            while sieve[0][0] == n:
                m,p = heapq.heappop(sieve)
                heapq.heappush(sieve, (m+2 * p,p) )
            
        n = n + 2

cachedprimes = []
cachedprimegen = sieve()

def genprimes():
    ndx = 0
    while True:
        while len(cachedprimes) <= ndx:
            cachedprimes.append(next(cachedprimegen))
        yield cachedprimes[ndx]
        ndx = ndx + 1

def factor(n):
    output = []
    for p in genprimes():
        factors = 0
        while n % p == 0:
            n = n // p
            factors = factors + 1
        if factors:
            output.append( (p,factors) )
        if n == 1:
            return output


def numpresents2(c):
    output = 1
    for p,factors in factor(c):
        pp = 1
        psum = 1
        for f in range(1,factors+1):
            pp = pp * p
            psum = psum + pp
        #print("  p: %s  factors: %s  psum:%s" % (p,factors,psum,))
        output *= psum
    #print("%s -> %s" % (c,output,))
    return output * 10
    
if args.p1:
    print("Doing part 1")

    maxpr = 1
    for c in itertools.count(1):
        pr = numpresents2(c)
        maxpr = max(maxpr,pr)
        if c % 10000 == 0:
            print("C: %s  P: %s (%s)" % (c,pr,maxpr,))
        if pr >= target:
            print("Enough: %s" % (c,))
            break

def genpresents2():
    elves = []
    house = 1
    
    while True:
        output = 0

        heapq.heappush( elves, (house, house, 50) )
        
        while elves[0][0] == house:
            h,enum,erem = heapq.heappop(elves)

            output = output + enum * 11
            
            if erem > 1:
                heapq.heappush( elves, (house + enum, enum, erem - 1) )

        yield (house,output)
        house = house + 1
        
    
if args.p2:
    print("Doing part 2")

    maxpr = 1
    for house,presents in genpresents2():
        if presents > maxpr:
            maxpr = presents 
            print("House: %s  Presents: %s" % (house,presents,))
        
        if presents >= target:
            print("House: %s  Presents: %s" % (house,presents,))
            break
