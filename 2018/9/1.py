#!/usr/bin/env pypy

import argparse, re, collections

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

lineRe = re.compile("([0-9]+) players; last marble is worth ([0-9]+) points")

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    players = int(m.group(1))
    lastpoints = int(m.group(2))

print("Players: %s  last marble: %s" % (players,lastpoints,))

def highscore(players,lastpoints):
    nummarbles = lastpoints
    marbles = collections.deque()
    marbles.append(0)
    nextmarble = 1
    scores = [0] * players
    for m in range(1,nummarbles+1):
        p = m % players
        if m % 23 == 0:
            scores[p] += m
            marbles.rotate(6)
            scores[p] += marbles.pop()
        else:
            marbles.rotate(-2)
            marbles.appendleft(m)
        #print("Marble: %s Player: %s Scores: %s Marbles: %s" % (m,p,scores,marbles,))
        
    print("high score: %s" % (max(scores),))
        
if args.p1:
    print("Doing part 1")

    highscore(players,lastpoints)
    
if args.p2:
    print("Doing part 2")

    highscore(players,lastpoints*100)
