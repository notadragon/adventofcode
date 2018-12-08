#!/usr/bin/env python

import re, itertools

lineRe = re.compile("(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")

alldeer = set()

class Deer():
    def __init__(self,name,speed,endurance,resttime):
        self.name = name
        self.speed = speed
        self.endurance = endurance
        self.resttime = resttime
        self.laptime = self.endurance + self.resttime
        self.score = 0
        
    def __str__(self):
        return "%s Speed:%s End:%s Resttime:%s AvgSpeed:%0.3f" % (self.name,self.speed,self.endurance,self.resttime,self.avgSpeed(),)

    def avgSpeed(self):
        return (self.speed * self.endurance) / (0.0 + self.laptime)

    def distance(self,time):
        
        laps = time / self.laptime
        rem = time - (self.laptime * laps)

        return laps * self.endurance * self.speed + self.speed * min(rem,self.endurance)
    
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)
        continue
    
    reindeer = m.group(1)
    speed = int(m.group(2))
    endurance = int(m.group(3))
    resttime = int(m.group(4))

    alldeer.add(Deer(reindeer,speed,endurance,resttime));

fastest = None
farthest = 0
for deer in alldeer:
    d = deer.distance(2503)
    if d > farthest:
        fastest = deer
        farthest = d
    print "%s:%s" % (deer,deer.distance(2503),)

print "Fastest:%s Distance:%s" % (fastest.name,farthest,)
    
for x in range(1,2504):
    fastest = set()
    farthest = 0
    for deer in alldeer:
        d = deer.distance(x)
        if d == farthest:
            fastest.add(deer)
        elif d > farthest:
            fastest.clear()
            fastest.add(deer)
            farthest = d
    print "x:%s fastest:%s (distance:%s)" % (x,[x.name for x in fastest],farthest,)
    for deer in fastest:
        deer.score = deer.score + 1

for deer in alldeer:
    print "Deer:%s Score:%s" % (deer.name,deer.score,)
