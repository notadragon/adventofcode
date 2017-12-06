#!/usr/bin/env python

import re, md5

floorRe = re.compile("The ([a-z]+) floor contains (?:(?:nothing relevant)|((?:a [a-z -]+,? )+)and (a [a-z -]+))\\.")
genRe = re.compile("([a-z]+) generator")
chipRe = re.compile("([a-z]+)-compatible microchip")

floorNames = { "first":0, "second":1, "third":2, "fourth":3, }

contents={}

class Generator:
    def __init__(self,t):
        self.t = t

    def __repr__(self):
        return "Gen:%s" % (self.t,)

    def putState(self,state,f):
        state.generators[self.t]=f
        state.types.add(self.t)
        
class Chip:
    def __init__(self,t):
        self.t = t

    def __repr__(self):
        return "Chip:%s" % (self.t,)

    def putState(self,state,f):
        state.chips[self.t] = f
        state.types.add(self.t)
        
class State:
    def __init__(self):
        self.elevator = 0
        self.chips = {}
        self.generators = {}

        self.types = set()
        self.moves = []
        
    def show(self):
        print "Steps: %s" % (len(self.moves),)
        for m in self.moves:
            print "  %s" % (m,)
        for i in range(0,4):
            f = "F%s " % (i,)
            if i == self.elevator:
                f += "E  "
            else:
                f += "   "
            for t in self.types:
                if self.generators[t] == i:
                    f += "%sG " % (t[0],)
                else:
                    f += ".  "
                if self.chips[t] == i:
                    f += "%sM " % (t[0],)
                else:
                    f += ".  " 
            print f

    def valid(self):
        for t in self.types:
            chipFloor = self.chips[t]
            genFloor = self.generators[t]

            if chipFloor == genFloor:
                continue

            for t2,f in self.generators.items():
                if chipFloor == f and t != t2:
                    return False
        return True

    def finished(self):
        if self.elevator != 3:
            return False
        for v in self.chips.values():
            if v != 3:
                return False
        for v in self.generators.values():
            if v != 3:
                return False
        return True
    
    def copy(self):
        out = State()
        out.elevator = self.elevator
        out.types = self.types
        out.chips = self.chips.copy()
        out.generators = self.generators.copy()
        out.moves = self.moves[:]

        return out
    
    def move(self,m):
        f = m[0]
        out = self.copy()
        if f < 0 or f > 3 or (f != self.elevator-1 and f != self.elevator+1):
            raise "Invalid target floor: %s" % (f,)

        out.elevator = f

        for mi in m[1:]:
            t = mi[1:]
            mg = mi[0]
            if mg == "G":
                if self.generators[t] != self.elevator:
                    raise "%s gen not on current floor" % (t,)
                out.generators[t] = f
            else:
                if self.chips[t] != self.elevator:
                    raise "%s chip not on current floor" % (t,)
                out.chips[t] = f

        out.moves.append(m)
                
        return out
        
    def currentFloor(self):
        currentFloor = []
        for t,f in self.chips.items():
            if f == self.elevator:
                currentFloor.append("M%s" % (t,))
        for t,f in self.generators.items():
            if f == self.elevator:
                currentFloor.append("G%s" % (t,))
        return currentFloor

    def getVal(self):
        out = self.elevator
        for t in self.types:
            tVal = (self.chips[t] << 2) | self.generators[t]
            out = (out << 4) | tVal
        return out
        
for l in open("input").readlines():
    l = l.strip()

    m = floorRe.match(l)

    if m:
        f = m.group(1)
        items = []
        i1=m.group(2)
        if i1:
            for i in i1.split(","):
                if i:
                    i = i.strip()[2:]
                    if i:
                        items.append(i)
        i2 = m.group(3)
        if i2:
            i2 = i2.strip()[2:]
            if i2:
                items.append(i2)

        f = floorNames[f]

        items2 = []
        for i in items:
            m = genRe.match(i)
            if m:
                items2.append(Generator(m.group(1)))
            else:
                m = chipRe.match(i)
                if m:
                    items2.append(Chip(m.group(1)))
                
        print "FLOOR: %s ITEMS: %s" % (f,items2,)

        contents[f] = items2
        
        continue

    print l

state = State()
for f,items in contents.items():
    for i in items:
        i.putState(state,f)


state.show()

step = 0
states = [state,]
winState = None
seenStates = set()

def pickMovables(currentFloor):
    for i in range(0,len(currentFloor)):
        yield( (currentFloor[i],) )
        for j in range(i+1,len(currentFloor)):
            yield(currentFloor[i],currentFloor[j],)        

while not winState:

    print "Step %s States: %s Seen: %s" % (step,len(states),len(seenStates),)
        
    nextStates = []

    for s in states:
        currentFloor = s.currentFloor()

        for items in pickMovables(currentFloor):
            if s.elevator > 0:
                m = (s.elevator -1,) + items
                nextState = s.move(m)
                nextVal = nextState.getVal()
                if nextState.valid() and nextVal not in seenStates:
                    nextStates.append(nextState)
                    seenStates.add(nextVal)
            if s.elevator < 3:
                m = (s.elevator +1,) + items
                nextState = s.move(m)
                nextVal = nextState.getVal()
                if nextState.valid() and nextVal not in seenStates:
                    nextStates.append(nextState)
                    seenStates.add(nextVal)

    states = nextStates
    step = step + 1

    for s in nextStates:
        if s.finished():
            winState = s
            

winState.show()
    
