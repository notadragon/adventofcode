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

lineRe = re.compile("\\[([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+)] (?:(falls asleep)|(wakes up)|(Guard #([0-99]+) begins shift))")

days = set()
states = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line

    ltime = ( int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), )
    if ltime[3] > 12:
        day = ltime[0:2] + (ltime[2]+1,)
    else:
        day = ltime[0:3]
        days.add(day)
    if m.group(6):
        action = ("sleep",)
    elif m.group(7):
        action = ("awake",)
    elif m.group(8):
        action = ("duty", int(m.group(9)), )

    states.append( ( ltime, action, ) )

#print("States: %s" % (states,))
#print("Days: %s" % (days,))

if True:
    ops = sorted(states + [ ( d + (0,0) , ("midnight",)) for d in days] + [ ( d + (1,0) , ("oneam",)) for d in days] )

    guards = {}
    today = None
    minutes = None
    laststate = "."
    
    for ltime,action in ops:
        #print("%s - %s" % (ltime,action,))

        if action[0] == "duty":
            g = action[1]
            if g in guards:
                guard = guards[g]
            else:
                guard = []
                guards[g] = guard
        elif action[0] == "midnight":
            today = ltime[0:3]
            minutes = []
            laststate = "."
        elif action[0] == "awake":
            for i in range(len(minutes),ltime[4]):
                minutes.append(laststate)
            laststate = "."
        elif action[0] == "sleep":
            for i in range(len(minutes),ltime[4]):
                minutes.append(laststate)
            laststate = "#"
        elif action[0] == "oneam":
            for i in range(len(minutes),60):
                minutes.append(laststate)
            guard.append( ( today, "".join(minutes), ) )

    guardstats = []
    
if args.p1:
    print("Doing part 1")

    for g,guard in guards.items():
        sleeptime = sum( sum( 1 for c in s[1] if c == "#") for s in guard)
        count,minute = max( [ ( sum( 1 for s in guard if s[1][i] == "#" ), i) for i in range(0,60) ] )

        guardstats.append( (sleeptime,count,minute,g,guard,))
        
    guardstats.sort()
    #for sleeptime,count,minute,g,guard in guardstats:
    #    print("%s: sleeptime:%s min:%s-%s product:%s" % (g,sleeptime,minute,count,g*minute,))
    #
    #    for gd in guard:
    #        print("%04d-%02d-%02d %s" % (gd[0][0],gd[0][1],gd[0][2],gd[1],))

    print("Chosen guard: %s" % (guardstats[-1][3],))
    print("Chosen minute: %s" % (guardstats[-1][2],))
    print("Product: %s" % (guardstats[-1][3] * guardstats[-1][2],))
        
            
if args.p2:
    print("Doing part 2")

    guardstats = []
    
    for g,guard in guards.items():
        sleeptime = sum( sum( 1 for c in s[1] if c == "#") for s in guard)
        count,minute = max( [ ( sum( 1 for s in guard if s[1][i] == "#" ), i) for i in range(0,60) ] )

        guardstats.append( (count,sleeptime,minute,g,guard,))
        
    guardstats.sort()
    #for count,sleeptime,minute,g,guard in guardstats:
    #    print("%s: sleeptime:%s min:%s-%s product:%s" % (g,sleeptime,minute,count,g*minute,))
    #
    #    for gd in guard:
    #        print("%04d-%02d-%02d %s" % (gd[0][0],gd[0][1],gd[0][2],gd[1],))

    print("Chosen guard: %s" % (guardstats[-1][3],))
    print("Chosen minute: %s" % (guardstats[-1][2],))
    print("Product: %s" % (guardstats[-1][3] * guardstats[-1][2],))
        
