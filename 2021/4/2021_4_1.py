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

lineRe = re.compile("^(?:(\d+(?:,\d+)*)|(\d+(?: +\d+)*))$")

calls = []
boards = []
board = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        if board:
            boards.append(board)
            board = None
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))

    #print(f"{x} --- {m.group(1)} --- {m.group(2)}")
    
    # Process input line
    if m.group(1):
        calls = [ int(y) for y in x.split(",") ]
    else:
        if board == None:
            board = []
        board.append( [ int(y) for y in re.split(" +",x) ] )

if board:
    boards.append(board)
    board = None
    
#print(f"Calls: {len(calls)} - {calls}")
#print(f"Boards: {len(boards)} - {boards}")

def printBoards(boards):
    for b in boards:
        for r in b:
            rd = []
            for x in r:
                if x >= 0:
                    rd.append("%5d" % (x,))
                else:
                    rd.append("(%3d)" % (-x-1,))
            print("".join(rd))
        print("")

def isWinnerRow(b,r):
    for i in range(0,len(b[r])):
        if b[r][i] >= 0:
            return False
    return True

def isWinnerCol(b,c):
    for r in b:
        if r[c] >= 0:
            return False
    return True
        
def isWinner(b):
    for r in range(0,len(b)):
        if isWinnerRow(b,r):
            return True
    for c in range(0,len(b[0])):
        if isWinnerCol(b,c):
            return True
    return False
        
def winner(boards):
    for b in boards:
        if isWinner(b):
            return b;
    return None


def call(boards, c):
    newboards = []
    for b in boards:
        newb = []
        for r in b:
            newr = []
            for x in r:
                if x == c:
                    newr.append(-x-1)
                else:
                    newr.append(x)
            newb.append(newr)
        newboards.append(newb)
    return newboards

def score(b, c):
    return c * sum( [ x for r in b for x in r if x >= 0 ] )

if args.p1:
    print("Doing part 1")

    #printBoards(boards)

    pboards = boards
    
    for c in calls:
        #print(f"CALL: {c}")
        pboards = call(pboards, c)

        #printBoards(pboards)

        w = winner(pboards)
        if w:
            print("WINNER")
            printBoards( [w] )
            print("")
            print(f"SCORE: {score(w,c)}")
            break;
        
    
if args.p2:
    print("Doing part 2")

    pboards = boards
    for c in calls:
        pboards = call(pboards, c)

        if len(pboards) == 1:
            if isWinner(pboards[0]):
                print("Last Winner")
                printBoards(pboards)
                print("")
                print(f"SCORE: {score(pboards[0],c)}")
                break
        else:
            pboards = [ b for b in pboards if not isWinner(b) ]
            
