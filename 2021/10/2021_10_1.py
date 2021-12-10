#!/usr/bin/env python3

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

lineRe = re.compile("[\[\]\{\}\(\)]*")
data = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

delimpairs = {
    "{" : "}",
    "(" : ")",
    "[" : "]",
    "<" : ">"
    }
    
def errorNdx(chunk):
    delimstack = collections.deque()
    
    for i in range(0,len(chunk)):
        c = chunk[i]
        if c in delimpairs:
            delimstack.append(delimpairs[c])
        else:
            expected = delimstack.pop()
            if c != expected:
                rest = list(delimstack)
                rest.reverse()
                rest = [expected] + rest
                return (i,rest)
    rest = list(delimstack)
    rest.reverse()
    return (-1,rest)
    
if args.p1:
    print("Doing part 1")

    errorscores = {
        ")" : 3,
        "]" : 57,
        "}" : 1197,
        ">" : 25137,
        }

    score = 0
    for chunk in data:
        ndx,expected = errorNdx(chunk)
        if ndx < 0:
            #print(f"Valid: {chunk}")
            pass
        else:
            print(f"Expected {expected[0]} but got {chunk[ndx]} at index {ndx}: {chunk}")
            score += errorscores[chunk[ndx]]
    print(f"Final Score: {score}")
        
if args.p2:
    print("Doing part 2")

    scores = {
        ")" : 1,
        "]" : 2,
        "}" : 3,
        ">" : 4,
        }

    allscores = []
    
    for chunk in data:
        ndx,expected = errorNdx(chunk)
        if ndx >= 0:
            continue

        score = 0
        for c in expected:
            score = score * 5
            score = score + scores[c]
        expectedstr = "".join(expected)
        print(f" - {chunk} - Complete by adding {expectedstr} - score: {score}")
        allscores.append(score)

    allscores.sort()
    #print(f"Scores {allscores}")
    finalscore = allscores[ (len(allscores) ) // 2 ]
    print(f"Final Score {finalscore}")
