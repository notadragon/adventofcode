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

lineRe = re.compile("^(Time|Distance):(.*)$")

times = None
distances = None

times2 = None
distances2 = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line

    if m.group(1) == "Time":
        times = tuple( int(x) for x in m.group(2).split(" ") if x.strip() )
        times2 = ( int(m.group(2).replace(" ","")), )
    elif m.group(1) == "Distance":
        distances = tuple( int(x) for x in m.group(2).split(" ") if x.strip() )
        distances2 = ( int(m.group(2).replace(" ","")), )

print(f"Times: {times} ({times2})")
print(f"Distances: {distances} ({distances2})")

def dist( racetime, buttontime):
    return (racetime - buttontime) * buttontime

                       
if args.p1:
    print("Doing part 1")

    product = 1
    
    for n in range(0,len(times)):
        time = times[n]
        distance = distances[n]

        wins = 0
        for i in range(0,time+1):
            d = dist(time,i)
            if d > distance:
                wins = wins + 1
                #print(f"Hold the button for {i} at the start of the race.  Then, the boat will travel at a speed of {i} for {time-i}, raching a total distance traveled of {d}")

                
        print(f"There are {wins} ways to win this race.")
        product = product * wins

    print(f"There are {product} ways to win.")
    
if args.p2:
    print("Doing part 2")

    product = 1
    
    for n in range(0,len(times2)):
        time = times2[n]
        distance = distances2[n]

        wins = 0
        for i in range(0,time+1):
            d = dist(time,i)
            if d > distance:
                wins = wins + 1
                #print(f"Hold the button for {i} at the start of the race.  Then, the boat will travel at a speed of {i} for {time-i}, raching a total distance traveled of {d}")

                
        print(f"There are {wins} ways to win this race.")
        product = product * wins

    print(f"There are {product} ways to win.")
