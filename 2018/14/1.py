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
    inval = int(x)

print("Inval: %s" % (inval,))

def step(state):
    poses, scores = state

    newrecipes = scores[poses[0]] + scores[poses[1]]
    if newrecipes < 10:
        scores.append( newrecipes )
    else:
        scores.append( newrecipes / 10 )
        scores.append( newrecipes % 10 )

    poses[0] = (poses[0] + scores[poses[0]] + 1) % (len(scores))
    poses[1] = (poses[1] + scores[poses[1]] + 1) % (len(scores))
        
    return (poses, scores)


def show(state):
    poses, scores = state

    toshow = list([" %d " % (s,) for s in scores])
    toshow[poses[0]] = "(%d)" % (scores[poses[0]],)
    toshow[poses[1]] = "[%d]" % (scores[poses[1]],)
    
    print("".join(toshow))


    
if args.p1:
    print("Doing part 1")

    poses = [ 0, 1 ]
    scores = [ 3, 7 ]

    state = (poses,scores,)

    while len(state[1]) < inval+10:
        state = step(state)
    nextvals = state[1][inval:inval+10]
    print("Next10: %s" % ("".join([str(x) for x in nextvals]),))
    
if args.p2:
    print("Doing part 2")

    ivals = [ int(x) for x in str(inval) ]

    poses = [ 0, 1 ]
    scores = [ 3, 7 ]
    state = (poses,scores,)
    
    while True:
        if state[1][-len(ivals):] == ivals:
            #show(state)
            print("len(state): %s Before: %s" % (len(state[1]),len(state[1]) - len(ivals),))
            break
        elif state[1][-len(ivals)-1:-1] == ivals:
            #show(state)
            print("len(state): %s Before: %s" % (len(state[1]),len(state[1]) - len(ivals) - 1,))
            break
        state = step(state)
