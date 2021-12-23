#!/usr/bin/env pypy3

import argparse, re, itertools, collections, queue

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

lineRe = re.compile("[\.#A-Z ]+")

data = []

for x in open(args.input).readlines():
    x = x.rstrip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    data.append(x)

def findPath(initstate, finalstate):
    movecosts = {
        "A" : 1,
        "B" : 10,
        "C" : 100,
        "D" : 1000,
    }

    roomids = {
        "A" : 0,
        "B" : 1,
        "C" : 2,
        "D" : 3,
    }

    # 8 9    10   11   12    13 14
    #      0    1    2    3
    #      4    5    6    7

    numspaces = 15

    def initdarray():
        output = [ [0] * numspaces for x in range(0,numspaces) ]
        
        for room in ( (8,9), (13,14), (0,4), (1,5), (2,6), (3,7),  ):
            output[room[0]][room[1]] = 1
            output[room[1]][room[0]] = 1

        for hall in ( (9,0), (9,10),
                      (10,0), (10,1), (10,11),
                      (11,1), (11,2), (11,12),
                      (12,2), (12,3), (12,13),
                      (13,3), ):
            output[hall[0]][hall[1]] = 2
            output[hall[1]][hall[0]] = 2

        return output
        
    darray = initdarray()


    def show(state):
        print("#############")
        print(f"#{state[8]}{state[9]}.{state[10]}.{state[11]}.{state[12]}.{state[13]}{state[14]}#")
        print(f"###{state[0]}#{state[1]}#{state[2]}#{state[3]}###")
        print(f"  #{state[4]}#{state[5]}#{state[6]}#{state[7]}#")
        print("  #########")

    costs = { }

    tosearch = queue.PriorityQueue()
    tosearch.put( (0,initstate) )

    showcost = 0
    
    while not tosearch.empty() and not finalstate in costs:
        npath = tosearch.get()

        cost = npath[0]
        lastpos = npath[-1]
        
        if lastpos in costs:
            continue
        costs[lastpos] = cost

        if lastpos == finalstate:
            return npath

        if cost >= showcost + 100:
            print(f"COST: {cost}")
            showcost = cost
            show(lastpos)

        for i in range(0,len(lastpos)):
            if lastpos[i] != ".":
                continue

            for j in range(0,len(lastpos)):
                if i == j:
                    continue
                
                movesteps = darray[i][j] 
                if movesteps == 0:
                    continue

                moving = lastpos[j]
                if moving == ".":
                    continue

                targetroom = roomids[moving]
                if j == targetroom + 4:
                    # in back of target room, stay.
                    continue
                
                if j == targetroom and lastpos[j+4] == moving:
                    # target room is full and good, stay.
                    continue
                    
                if i < 4:
                    if i != targetroom:
                        if j != i+4:
                            # never enter wrong room
                            continue
                    else:
                        if j == i+4:
                            # don't back out of target room
                            continue
                        # only enter target room if back of target room is empty or correct
                        if lastpos[i+4] != moving and lastpos[i+4] != '.':
                            continue
                elif i < 8:
                    if i != targetroom + 4:
                        # never go backwards into wrong room
                        continue
                

                newpos = list(lastpos)
                newpos[i] = moving
                newpos[j] = "."
                newcost = cost + movesteps * movecosts[moving]

                newpos = tuple(newpos)

                if not newpos in costs:
                    tosearch.put( (newcost, newpos) )
        

def findPath2(initstate, finalstate):
    movecosts = {
        "A" : 1,
        "B" : 10,
        "C" : 100,
        "D" : 1000,
    }

    roomids = {
        "A" : 0,
        "B" : 1,
        "C" : 2,
        "D" : 3,
    }

    # 16 17  18   19   20   21 22
    #      0    1    2    3
    #      4    5    6    7
    #      8    9   10   11
    #     12   13   14   15

    numspaces = 23

    def initdarray():
        output = [ [0] * numspaces for x in range(0,numspaces) ]
        
        for room in ( (16,17), (21,22), (0,4,8,12), (1,5,9,13), (2,6,10,14), (3,7,11,15),  ):
            for n in range(0,len(room)-1):
                output[room[n]][room[n+1]] = 1
                output[room[n+1]][room[n]] = 1

        for hall in ( (17,0), (17,18),
                      (18,0), (18,1), (18,19),
                      (19,1), (19,2), (19,20),
                      (20,2), (20,3), (20,21),
                      (21,3), ):
            output[hall[0]][hall[1]] = 2
            output[hall[1]][hall[0]] = 2

        return output
        
    darray = initdarray()


    def show(state):
        print("#############")
        print(f"#{state[16]}{state[17]}.{state[18]}.{state[19]}.{state[20]}.{state[21]}{state[22]}#")
        print(f"###{state[0]}#{state[1]}#{state[2]}#{state[3]}###")
        print(f"  #{state[4]}#{state[5]}#{state[6]}#{state[7]}#")
        print(f"  #{state[8]}#{state[9]}#{state[10]}#{state[11]}#")
        print(f"  #{state[12]}#{state[13]}#{state[14]}#{state[15]}#")
        print("  #########")


    def behind(state, roompos):
        roompos = roompos + 4
        while roompos < 16:
            yield state[roompos]
            roompos = roompos + 4

    def inroom(state, roomid):
        for c in behind(state,roomid-4):
            yield c
        
    costs = { }

    tosearch = queue.PriorityQueue()
    tosearch.put( (0,initstate) )

    showcost = 0
    
    while not tosearch.empty() and not finalstate in costs:
        npath = tosearch.get()

        cost = npath[0]
        lastpos = npath[-1]
        
        if lastpos in costs:
            continue
        costs[lastpos] = cost

        if lastpos == finalstate:
            return npath

        if cost >= showcost + 100:
            print(f"COST: {cost}")
            showcost = cost
            show(lastpos)

        for i in range(0,len(lastpos)):
            if lastpos[i] != ".":
                continue

            for j in range(0,len(lastpos)):
                if i == j:
                    continue
                
                movesteps = darray[i][j] 
                if movesteps == 0:
                    continue

                moving = lastpos[j]
                if moving == ".":
                    continue

                targetroom = roomids[moving]
                if j == targetroom + 12:
                    # in back of target room, stay.
                    continue

                if j == targetroom + 8 and lastpos[j+4] == moving:
                    continue

                if j == targetroom + 4 and lastpos[j+4] == moving and lastpos[j+8] == moving:
                    continue
                
                if j == targetroom and lastpos[j+4] == moving and lastpos[j+8] == moving and lastpos[j+12] == moving:
                    # target room is full and good, stay.
                    continue

                if i < 16:
                    iroom = i % 4

                    if iroom != targetroom:
                        # only back out of other rooms
                        if j >= 16 or j < i:
                            continue
                    elif j >= 16:
                        badcontents = ( c for c in inroom(lastpos,iroom) if c != moving and c != '.' )

                        if badcontents:
                            continue
                    elif j > i:
                        # check if able to move out of right room (bad thing behind us)
                        
                        badcontents = (c for c in behind(lastpos,j) if c != moving and c != '.' )

                        if not badcontents:
                            continue
                    else:
                        # check if we can go deeper into the room (no bad thing behind us)

                        badcontents = (c for c in behind(lastpos,j) if c != moving and c != '.' )

                        if badcontents:
                            continue

                newpos = list(lastpos)
                newpos[i] = moving
                newpos[j] = "."
                newcost = cost + movesteps * movecosts[moving]

                newpos = tuple(newpos)

                if not newpos in costs:
                    tosearch.put( (newcost, newpos) )
        

                    
if args.p1:
    print("Doing part 1")

    initstate = []
    for d in data:
        for c in d:
            if c in "ABCD":
                initstate.append(c)
    for i in range(0,7):
        initstate.append(".")
    initstate = tuple(initstate)

    print(f"{initstate}")


    finalstate = ( 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', '.', '.', '.', '.', '.', '.', '.', )

    path = findPath(initstate, finalstate)

    print(f"Best path: {path}")
    
if args.p2:
    print("Doing part 2")

    newlines = [ "#D#C#B#A#",
                 "#D#B#A#C#", ]

    initstate = []
    for d in newlines:
        for c in d:
            if c in "ABCD":
                initstate.append(c)
    for d in data:
        for c in d:
            if c in "ABCD":
                initstate.append(c)
    for i in range(0,7):
        initstate.append(".")
    initstate = tuple(initstate)
    
    finalstate = ( 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D',
                   'A', 'B', 'C', 'D', '.', '.', '.', '.', '.', '.', '.', )


    path = findPath2(initstate, finalstate)

    print(f"Best path: {path}")
