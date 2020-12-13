#!/usr/bin/env pypy

import argparse, re, itertools, collections

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

ts = None
sched = []

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
    if not ts:
        ts = int(x)
        continue
    if not sched:
        sched = x.split(",")
        continue
    print("Invalid line: %s" % (x,))    

print("Ts: %s" % (ts,))
print("Shed: %s" % (sched,))
    
if args.p1:
    print("Doing part 1")

    bestbus = None
    bestbustime = None
    for i in range(0,len(sched)):
        if sched[i] == "x":
            continue
        busid = int(sched[i])
        busts = (ts // busid) * busid
        if busts < ts:
            busts += busid
        #print("Bus: %s  Time: %s" % (busid, busts, ))
        if bestbustime == None or busts < bestbustime:
            bestbustime = busts
            bestbus = busid
    print("Best Bus ID: %s at %s" % (bestbus,bestbustime,))
    print("Wait Time: %s" % (bestbustime - ts,))
    print("Result: %s" % ( (bestbustime - ts) * bestbus,))
    
if args.p2:
    print("Doing part 2")

    offsets = {}
    primes = []
    M = 1
    for i in range(0,len(sched)):
        if sched[i] != "x":
            primes.append(int(sched[i]))
            offsets[primes[-1]] = i
            M *= primes[-1]

    print("M: %s" % (M,))

    def euclidean(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = euclidean( b % a, a)
            #print("%s -> %s" % ((a,b,),(g,y,x,),))
            return (g, x - (b // a) * y, y)    
    
    def inverse(a,m):
        # return b such that b * a =~ 1 mod m
        g, y, x = euclidean(a, m)
        #print("%s -> %s -> %s" % ( (a,m), (g,y,x), y%m, ) )
        return y % m

    # R + off_i =~ 0 mod m_i
    # R =~ -off_i mod m_i
    # R =~ -off_i * b_i * N/m_i mod m_i
    
    inverses = []
    R = 0
    for m_i in primes:
        # b_i * M/m_i =~ 1 mod m
        b_i = inverse(M / m_i, m_i)
        
        inverses.append(b_i)

        off_i = offsets[m_i]
        R += - b_i * off_i * M / m_i

        print("m_i: %s  M / m_i: %s  b_i: %s off_i: %s" % (m_i, M / m_i, b_i, off_i))
    R %= M
        
    print("Total: %s" % (R,))
