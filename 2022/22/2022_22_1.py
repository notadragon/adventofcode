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

lineRe = re.compile("^(?:([ \.#]+)|([0-9LR]+))$")
grid = []
data = None

for x in open(args.input).readlines():
    x = x.rstrip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(1):
        grid.append(m.group(1))
    else:
        data = x

#for l in grid:
#    print(l)
#print(data)
                    
board = {}
for y in range(0,len(grid)):
    for x in range(0,len(grid[y])):
        c = grid[y][x]
        if c == "." or c == "#":
            board[ (x,y) ] = c

ops = re.findall( "[0-9]+|[LR]", data )
    
facings = (
    ( ">", (1,0),  ),
    ( "v", (0,1),  ),
    ( "<", (-1,0), ),
    ( "^", (0,-1), ),
    )


def buildFlatAdjacencies(board):
    minx = min(loc[0] for loc in board.keys())
    maxx = max(loc[0] for loc in board.keys())
    miny = min(loc[1] for loc in board.keys())
    maxy = max(loc[1] for loc in board.keys())

    adjacencies = {}

    for x in range(minx,maxx+1):
        col = list([ loc for loc in board.keys() if loc[0] == x ])
        col.sort()

        for i in range(0,len(col)):
            loc = col[i]
        
            if i == 0:
                up = col[-1]
            else:
                up = col[i-1]
            if i == len(col)-1:
                down = col[0]
            else:
                down = col[i+1]

            adjacencies[ (loc, 3) ] = (up, 3)
            adjacencies[ (loc, 1) ] = (down, 1)

    for y in range(miny, maxy+1):
        row = list([ loc for loc in board.keys() if loc[1] == y ])
        row.sort()

        for i in range(0,len(row)):
            loc = row[i]
            if i == 0:
                left = row[-1]
            else:
                left = row[i-1]
            if i == len(row)-1:
                right = row[0]
            else:
                right = row[i+1]

            adjacencies[ (loc, 0) ] = (right, 0)
            adjacencies[ (loc, 2) ] = (left, 2)

    return adjacencies

def showboard(board, path):
    minx = min(loc[0] for loc in board.keys())
    maxx = max(loc[0] for loc in board.keys())
    miny = min(loc[1] for loc in board.keys())
    maxy = max(loc[1] for loc in board.keys())


    for y in range(miny,maxy+1):
        line = []
        for x in range(minx,maxx+1):
            loc = (x,y)
            if loc in path:
                line.append(path[loc])
            elif loc in board:
                line.append(board[loc])
            else:
                line.append(" ")
        print("".join(line))

def followops(ops, board, adjacencies, startloc, startfacing):
    print(f"Starting Location: {startloc} : {startfacing}")

    path = {}
    
    loc = startloc
    facing = startfacing

    path[loc] = facings[facing][0]
    
    for op in ops:
        if op == "L":
            facing = (facing - 1) % len(facings)
        elif op == "R":
            facing = (facing + 1) % len(facings)
        else:
            op = int(op)
            for i in range(0,op):
                nextloc,nextfacing = adjacencies[ (loc,facing) ]
                if nextloc in board and board[nextloc] == ".":
                    loc = nextloc
                    facing = nextfacing
                    path[loc] = facings[facing][0]
                else:
                    break
        path[loc] = facings[facing][0]

    showboard(board,path)

    return (loc, facing)

    
        
if args.p1:
    print("Doing part 1")

    adjacencies = buildFlatAdjacencies(board)
    
    miny = min( loc[1] for loc in board.keys() )
    startloc = min( loc for loc in board.keys() if loc[1] == miny )
    startfacing = 0
    
    loc,facing = followops(ops, board, adjacencies, startloc, startfacing)

    print(f"Final Location: {loc}  Final Facing: {facing}")
    password = 1000 * (loc[1]+1) + 4 * (loc[0]+1) + facing
    print(f"Password: {password}")

def iterateedge(board, startloc, startfacing, facingdelta = 1):
    loc = startloc
    facing = startfacing
    while True:
        yield (loc,facing)

        forwarddelta = facings[facing][1]
        adjdelta = facings[ (facing + facingdelta)%4 ][1]
        
        nextloc = None
        nextfacing = None

        if not nextloc:
            # check for inside corner
            cornerloc = ( loc[0] + forwarddelta[0] + adjdelta[0], loc[1] + forwarddelta[1] + adjdelta[1] )
            if cornerloc in board:
                nextloc = cornerloc
                nextfacing = (facing - facingdelta) % 4

        if not nextloc:
            # check about contuing adj:
            adjloc = (loc[0] + adjdelta[0], loc[1] + adjdelta[1])
            if adjloc in board:
                nextloc = adjloc
                nextfacing = facing

        if not nextloc:
            # turn adj
            nextloc = loc
            nextfacing = (facing + facingdelta) % 4

        if nextloc == startloc and nextfacing == startfacing:
            break

        loc = nextloc
        facing = nextfacing
        
        
    
def buildCubeAdjacencies(board):
    adjacencies = buildFlatAdjacencies(board)

    tozip = []
    zippath = {}
    
    miny = min( loc[1] for loc in board.keys() )
    startloc = min( loc for loc in board.keys() if loc[1] == miny )
    startfacing = 3

    insidecorners = []
    outsidecorners = []

    outsidecorners.append( (startloc, 1, 0) )  # location, left, right
    prevloc = None
    prevfacing = None
    
    for loc, facing in iterateedge(board, startloc, startfacing):
        tozip.append( (loc, facing) )
        zippath[loc] = facings[facing][0]

        if prevfacing != None and facing == ((prevfacing-1) % 4):
            # inside corner
            prevfacingdelta = facings[ (prevfacing+1)%4 ][1]
            cornerloc = ( prevloc[0] + prevfacingdelta[0], prevloc[1] + prevfacingdelta[1] )
            
            insidecorners.append( (cornerloc, (prevfacing-1) % 4, (facing+1) % 4) )

        if prevfacing != None and facing == ((prevfacing+1) % 4):
            # outside corner
            outsidecorners.append( (loc, (prevfacing-1)%4, (facing+1)%4) )

        prevloc = loc
        prevfacing = facing

    for loc,f1,f2 in insidecorners:
        zippath[loc] = "C"
    for loc,f1,f2 in outsidecorners:
        zippath[loc] = "O"

    for loc,leftfacing,rightfacing in insidecorners:
        #print(f"Starting at corner: {loc} left: {facings[leftfacing][0]} right: {facings[rightfacing][0]}")
        leftdelta = facings[leftfacing][1]
        leftloc = (loc[0] + leftdelta[0], loc[1] + leftdelta[1])
        rightdelta = facings[rightfacing][1]
        rightloc = (loc[0] + rightdelta[0], loc[1] + rightdelta[1])

        leftedge = list(iterateedge(board, leftloc, (leftfacing+1)%4, -1))
        rightedge = list(iterateedge(board, rightloc, (rightfacing-1)%4, 1))

        #print(f"Left Edge: {leftedge}")
        #print(f"Right Edge: {rightedge}")
        
        for i in range(0,min(len(leftedge),len(rightedge))):
            leftout = leftedge[i]
            rightout = rightedge[i]
            if i > 0:
                isleftoutside = leftout[0] == leftedge[i-1][0]
                isrightoutside = rightout[0] == rightedge[i-1][0]

                if isleftoutside and isrightoutside:
                    break

            #print(f"Tie {leftout} to {rightout}")
            zippath[ leftout[0] ] = "*"
            zippath[ rightout[0] ] = "*"

            rightin = ( rightout[0], (rightout[1]+2) % 4)
            leftin = ( leftout[0], (leftout[1]+2) % 4)

            adjacencies[leftout] = rightin
            adjacencies[rightout] = leftin
        
    #showboard(board, zippath)
    
    return adjacencies
    
                    
if args.p2:
    print("Doing part 2")

    adjacencies = buildCubeAdjacencies(board)
    
    miny = min( loc[1] for loc in board.keys() )
    startloc = min( loc for loc in board.keys() if loc[1] == miny )
    startfacing = 0
    
    loc,facing = followops(ops, board, adjacencies, startloc, startfacing)

    print(f"Final Location: {loc}  Final Facing: {facing}")
    password = 1000 * (loc[1]+1) + 4 * (loc[0]+1) + facing
    print(f"Password: {password}")

    
