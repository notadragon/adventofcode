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

lineRe = re.compile("^Blueprint ([0-9]+): (.*)$")
robotRe = re.compile("^Each ([a-z]+) robot costs (.*)$")

blueprints = {}
typeids = {
    "ore" : 1,
    "clay" : 2,
    "obsidian" : 3,
    "geode" : 4,
    }
typenames = { tid : t for t,tid in typeids.items() }

tactions = {
    "ore" : "collecting",
    "clay" : "collecting",
    "obsidian" : "collecting",
    "geode" : "cracking",
    }

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    blueprintid = int(m.group(1))
    robots = m.group(2)
    blueprintdata = {}

    for robot in robots.split("."):
        if not robot:
            continue
        robot = robot.strip()
        m2 = robotRe.match(robot)
        if not m2:
            print(f"Invalid robot costs: {robot}")

        rtype = m2.group(1)
        rtype = typeids[rtype]
        rvals = []
        for val in m2.group(2).split(" and "):
            num,ctype = val.split(" ")
            num = int(num)
            ctype = typeids[ctype]
            rvals.append( (num,ctype) )
        blueprintdata[rtype] = rvals
    blueprints[blueprintid] = blueprintdata

#for bid,bval in blueprints.items():
#    print(f"{bid} -> {bval}")

class State:
    def __init__(self, minutes):
        self.minutes = minutes
        self.items = [None] + [ (0,0) ] * 4

    def copy(self):
        output = State(self.minutes)
        output.items = self.items.copy()
        return output

    def count(self, itemid):
        return self.items[itemid][1]

    def countrobots(self, itemid):
        return self.items[itemid][0]

    def additems(self, itemid, diff):
        if diff != 0:
            current = self.items[itemid]
            self.items[itemid] = ( current[0], current[1] + diff, )

    def addrobot(self, itemid, num):
        if num != 0:
            current = self.items[itemid]
            self.items[itemid] = ( current[0] + num, current[1], )

    def canbuy(self, blueprintdata, op):
        bvals = blueprintdata.costs(op)
        for num,ctype in bvals:
            if self.count(ctype) < num:
                return False
        return True
            
    def advance(self, blueprintdata, op):
        if op > 0:
            opdata = self.items[op]
            maxcost = blueprintdata.maxcost(op)
            maxneeded = self.minutes * maxcost
            expected = opdata[1] + self.minutes * opdata[0]
            if maxneeded <= expected:
                return None

        waitminutes = 0
        if op > 0:
            minutesneeded = 0
            bvals = blueprintdata.costs(op)
            for num,ctype in bvals:
                cdata = self.items[ctype]
                if cdata[0] == 0:
                    return None
                needed = num - cdata[1]
                neededtime = max(0, (needed + cdata[0] - 1) // cdata[0])
                minutesneeded = max(minutesneeded, neededtime)
                #print(f"have {cdata[1]}, need {num}, wait {neededtime}")
            if minutesneeded >= self.minutes:
                return None

            waitminutes = minutesneeded
        else:
            waitminutes = self.minutes-1
            
        output = self.copy()

        if waitminutes > 0:
            #print(f"Waiting {waitminutes} minutes for {op}")
            output.minutes = output.minutes - waitminutes
            for itype in typeids.values():
                idata = output.items[itype]
                output.items[itype] = ( idata[0], idata[0] * waitminutes + idata[1])
                
        output.minutes = output.minutes - 1
        for itype in typeids.values():
            idata = output.items[itype]
            output.items[itype] = ( idata[0], idata[0] + idata[1], )

        if op > 0:
            bvals = blueprintdata.costs(op)
            for num,ctype in bvals:
                output.additems(ctype,-num)

        if op > 0:
            output.addrobot(op,1)

        #print(f"advance - {self} + op: {op} -> {output}")
        return output

    def __repr__(self):
        stuff = []
        for tid in typeids.values():
            tvals = self.items[tid]
            tname = typenames[tid]
            if tvals[0] != 0:
                stuff.append(f"{tvals[0]} {tname} robots")
            if tvals[1] != 0:
                stuff.append(f"{tvals[1]} {tname}")
        stuffstr = ", ".join(stuff)
        return f"Minutes: {self.minutes}, {stuffstr}"

allops = (4,3,2,1,0)
geodeid = typeids["geode"]

class BluePrintData:
    def __init__(self, blueprintid, blueprintdata):
        self.blueprintid = blueprintid        
        self.data = blueprintdata

        self.maxcosts = {}
        for bvals in self.data.values():
            for num,ctype in bvals:
                self.maxcosts[ctype] = max(self.maxcosts.get(ctype,0),num)
        self.maxcosts[geodeid] = 1000000

    def costs(self, itemid):
        return self.data[itemid]

    def maxcost(self, itemid):
        return self.maxcosts[itemid]
    

def bestState(blueprintdata, state):
    #print(f"bestState - State: {state}")
    if state.minutes <= 0:
        return (),state

    best = None
    bestpath = None
    for op in allops:
        nextstate = state.advance(blueprintdata,op)
        if not nextstate:
            continue

        rpath, rstate = bestState(blueprintdata, nextstate)
        if rstate == None:
            continue

        if best == None or best.count(geodeid) < rstate.count(geodeid):
            best = rstate
            bestpath = (0,) * (state.minutes - nextstate.minutes - 1) + (op,) + rpath

            #print(f"Best: {best}")

    return bestpath,best

def printOps(blueprintdata, ops):
    print(f"Ops: {ops}")
    items = {}
    for t,tid in typeids.items():
        items[tid] = [ 0, 0 ]
        if t == "ore":
            items[tid][0] = 1

    def descvals(bvals):
        output = []
        for num,ctype in bvals:
            output.append(f"{num} {typenames[ctype]}")
        return " and ".join(output)
            
    for i,op in enumerate(ops,1):
        
        print(f"==Minute {i}==")
        if op > 0:
            t = typenames[op]
            bvals = blueprintdata.costs(op)
            print(f"Spend {descvals(bvals)} to start building a {t}-{tactions[t]} robot.")

            for num,ctype in bvals:
                items[ctype][1] = items[ctype][1] - num
            
        for t,tid in typeids.items():
            tdata = items[tid]

            if tdata[0] > 0:
                tdata[1] = tdata[1] + tdata[0]
                tp = "s" if tdata[0] > 1 else ""
                cp = "s" if tdata[0] == 1 else ""
                print(f"{tdata[0]} {t}-{tactions[t]} robot{tp} collect{cp} {tdata[0]} ore; you now have {tdata[1]} {t}.")

        if op > 0:
            t = typenames[op]
            items[op][0] = items[op][0] + 1
            print(f"The new {t}-{tactions[t]} robot is ready; you now have {items[op][0]} of them.")

if args.p1:
    print("Doing part 1")

    state = State(24)
    state.addrobot(typeids["ore"],1)

    totalquality = 0
    for blueprintid, blueprintdata in blueprints.items():
        bps = BluePrintData(blueprintid, blueprintdata)
        ops,best = bestState(bps, state.copy())
        #printOps(bps,ops)
        qualitylevel = blueprintid * best.count(geodeid)
        totalquality = totalquality + qualitylevel
        print(f"Blueprintid: {blueprintid}  Geodes: {best.count(geodeid)}  Quality: {qualitylevel}")
    print(f"Total Quality: {totalquality}")
        
if args.p2:
    print("Doing part 2")

    state = State(32)
    state.addrobot(typeids["ore"],1)

    product = 1
    for blueprintid, blueprintdata in blueprints.items():
        if blueprintid > 3:
            continue
        bps = BluePrintData(blueprintid, blueprintdata)
        ops,best = bestState(bps, state.copy())
        #printOps(bps,ops)
        product *= best.count(geodeid)
        print(f"Blueprintid: {blueprintid}  Geodes: {best.count(geodeid)}")
    print(f"Geode product: {product}")
