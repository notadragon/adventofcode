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


def parseState(data):
    rooms = [ [], [], [], [], ["."] * 7, ]
    ndx = 0
    for d in data:
        for c in d:
            if c in "ABCD":
                rooms[ndx % 4].append(c)
                ndx = ndx + 1

    return tuple( tuple(r) for r in rooms )

def amphicount(state):
    output = 0
    for r in state:
        for c in r:
            if c in "ABCD":
                output = output + 1
    return output

sids = {}
nextsid = 1
def show(state):
    
    if state in sids:
        sid = sids[state]
    else:
        global nextsid
        sid = nextsid
        sids[state] = sid
        nextsid = nextsid + 1
        
    print(f"-------{sid}--------")
    
    print("#############")
    print(f"#{state[-1][0]}{state[-1][1]}.{state[-1][2]}.{state[-1][3]}.{state[-1][4]}.{state[-1][5]}{state[-1][6]}#")

    roomsize = amphicount(state) // 4
    for i in range(0,roomsize):
        row = []
        for r in range(0,4):
            rc = len(state[r])
            n  = i - (roomsize - rc)
            c = state[r][n] if n >= 0 else "."
            row.append(c)
        if i == 0:
            w = "##"
        else:
            w = "  "
        print(f"{w}#{row[0]}#{row[1]}#{row[2]}#{row[3]}#{w}")

    print("  #########")

def findPath(initstate):
    amphipodcount = amphicount(initstate)
    roomsize = amphipodcount // 4
    finalstate = ( ('A',) * roomsize, ('B',) * roomsize, ('C',) * roomsize, ('D',) * roomsize, ('.',) * 7, )

    costs = {}

    tosearch = queue.PriorityQueue()
    tosearch.put( (0, initstate) )

    def iscleanroom(r,c):
        for rc in r:
            if rc != c:
                #print(f"Dirty room! {r} {c}")
                return False
        #print(f"Clean room! {r} {c}")
        return True

    def clearpathlength(hallway, htarget, roomid):
        hallindex = roomid + 1
        if htarget <= hallindex:
            plen = 0
            for i in range(hallindex,htarget-1,-1):
                if hallway[i] != ".":
                    return None
                if i == 0 or i == 6:
                    plen = plen + 1
                else:
                    plen = plen + 2
            return plen
        else:
            plen = 0
            for i in range(hallindex+1,htarget+1):
                if hallway[i] != ".":
                    return None
                if i == 0 or i == 6:
                    plen = plen + 1
                else:
                    plen = plen + 2
            return plen

    def clearpathinlength(hallway, htarget, roomid):
        hallindex = roomid + 1
        plen = 1 if (htarget == 0 or htarget == 6) else 2
        if htarget <= hallindex:
            for i in range(htarget+1,hallindex+1):
                if hallway[i] != ".":
                    return None
                plen = plen + 2
        else:
            for i in range(htarget-1,hallindex,-1):
                if hallway[i] != ".":
                    return None
                plen = plen + 2
        return plen

    def clearroomlength(hallway, rfrom, rto):
        r1 = min(rfrom, rto)
        r2 = max(rfrom, rto)

        for i in range(2 + r1, 2 + r2 ):
            if hallway[i] != ".":
                return None

        return 2 + 2*(r2-r1)

    def movefromroom(state, roomid, htarget):
        newstate = list(state)
        moving = state[roomid][0]
        newstate[roomid] = newstate[roomid][1:]
        newstate[-1] = tuple( state[-1][i] if i != htarget else moving for i in range(0,7) )
        return tuple(newstate)

    def movetoroom(state, hfrom, roomid):
        newstate = list(state)
        moving = state[-1][hfrom]
        newstate[roomid] = (moving,) + newstate[roomid]
        newstate[-1] = tuple( state[-1][i] if i != hfrom else "." for i in range(0,7) )
        return tuple(newstate)

    def moveroomroom(state, rfrom, rto):
        newstate = list(state)
        moving = state[rfrom][0]
        newstate[rfrom] = state[rfrom][1:]
        newstate[rto] = (moving,) + state[rto]
        return tuple(newstate)

    verbose = False

    while not tosearch.empty() and not finalstate in costs:
        cost,state = tosearch.get()

        if state in costs:
            continue
        costs[state] = cost
        
        if verbose:
            print("")
            if state in sids:
                print(f"Checking from state {sids[state]} with cost {cost}")
            else:
                print(f"Checking from state with cost {cost}")
            show(state)

        #if any can be moved to final room that's it, no need to explore other options.
        found = False
        for roomid in range(0,4):
            if found:
                break
            
            roomcontents = chr(ord('A') + roomid)

            if iscleanroom(state[roomid],roomcontents) and len(state[roomid]) < roomsize:
                if verbose:
                    print(f"Move {roomcontents} into room {roomid} ({state[roomid]})")

                roomsteps = roomsize - len(state[roomid]) - 1
                
                for hfrom in range(0,7):
                    if state[-1][hfrom] == roomcontents:
                        plen = clearpathinlength(state[-1], hfrom, roomid)
                        if plen != None:
                            steps = plen + roomsteps
                            movingcost = movecosts[roomcontents]
                            movecost = movingcost * steps
                            newcost = cost + movecost
                            newstate = movetoroom(state, hfrom, roomid)

                            if verbose:
                                print(f"  From index {hfrom} with {plen}+{roomsteps} steps at cost {movecost} (total: {newcost})")
                                show(newstate)

                            tosearch.put( (newcost, newstate) )
                            found = True
                            break
                
                for otherroom in range(0,4):
                    if found:
                        break
                    if otherroom == roomid:
                        continue

                    if state[otherroom] and state[otherroom][0] == roomcontents:
                        plen = clearroomlength(state[-1], roomid, otherroom)
                        if plen != None:
                            otherroomsteps = roomsize - len(state[otherroom]) 
                            steps = plen + roomsteps + otherroomsteps

                            movingcost = movecosts[roomcontents]
                            movecost = movingcost * steps

                            newcost = cost + movecost
                            newstate = moveroomroom(state, otherroom, roomid)

                            if verbose:
                                print(f"  From room {otherroom} with {plen}+{otherroomsteps}+{roomsteps} steps at cost {movecost} (total: {newcost})")
                                show(newstate)

                            tosearch.put( (newcost, newstate) )
                            found = True
                            break

        if not found:
            for roomid in range(0,4):
                roomcontents = chr(ord('A') + roomid)                
                if not iscleanroom(state[roomid],roomcontents):
                    if verbose:
                        print(f"Move {state[roomid][0]} out of room {roomid} ({state[roomid]})")

                    roomsteps = roomsize - len(state[roomid])
                    moving = state[roomid][0]
                    movingcost = movecosts[moving]
                    for htarget in range(0,7):
                        plen = clearpathlength(state[-1], htarget, roomid)
                        if plen != None:
                            steps = plen + roomsteps
                            movecost = movingcost * steps
                            newcost = cost + movecost
                            newstate = movefromroom(state, roomid, htarget)

                            if verbose:
                                print(f"  To index {htarget} with {plen}+{roomsteps} steps at cost {movecost} (total: {newcost})")
                                show(newstate)

                            tosearch.put( (newcost, newstate) )

                    
                    
    if finalstate in costs:
        return costs[finalstate]
    else:
        return None
    
if args.p1:
    print("Doing part 1")

    initstate = parseState(data)

    show(initstate)

    path = findPath(initstate)

    print(f"Best path: {path}")
    
if args.p2:
    print("Doing part 2")

    newlines = [ "#D#C#B#A#",
                 "#D#B#A#C#", ]

    newdata = data[0:3] + newlines + data[3:]

    initstate = parseState(newdata)

    show(initstate)

    path = findPath(initstate)

    print(f"Best path: {path}")
