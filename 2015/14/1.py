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

lineRe = re.compile("(.*) can fly ([0-9]+) km/s for ([0-9]+) seconds, but then must rest for ([0-9]+) seconds.")

reindeer = {}
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue

    reindeer[m.group(1)] = ( int(m.group(2)), int(m.group(3)), int(m.group(4)),)

def travelled(r, time):
    speed,active,rest = r

    full = active + rest
    output = speed*active*(time/full)
    partialtime = time % full
    output += speed * min(partialtime,active)

    return output
    
    
print("Reindeer: %s" % (reindeer,))

if args.p1:
    print("Doing part 1")

    furthest = max( [ travelled(r,2503) for r in reindeer.values() ] )

    print("Furthest: %s" % (furthest,))
    
if args.p2:
    print("Doing part 2")

    state = {}
    for r in reindeer.keys():
        state[r] = [0,0]

    for i in range(0,2503):
        for r,rstats in reindeer.items():
            speed,active,rest = rstats
            full = active+rest
            if (i % full) < active:
                state[r][0] += speed

        furthest = max([rs[0] for rs in state.values()] )
        for rs in state.values():
            if rs[0] == furthest:
                rs[1] = rs[1] + 1

    print(state)
    winningpoints = max([rs[1] for rs in state.values()])
    print("Winning Points: %s" % (winningpoints,))
