#!/usr/bin/env python

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

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

valRe = re.compile("([a-z])=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>")

particles = []
for x in open(args.input).readlines():
    x = x.strip()

    vs = {}
    for v in x.split(", "):
        v = v.strip()
        m = valRe.match(v)
        if not m:
            vs = None
            break
        vs[m.group(1)] = (int(m.group(2)),int(m.group(3)),int(m.group(4)),)

    if not vs:
        print "Invalid line: %s" % (x,)
    else:
        particles.append(vs)

if args.p1:
    print "Doing part 1"

    slowest = []
    slowestaccel = 0
    for i in range(0,len(particles)):
        accel = particles[i]["a"]
        accelval = sum(abs(x) for x in accel)
        if not slowest or accelval < slowestaccel:
            slowest = [i,]
            slowestaccel = accelval
        elif accelval == slowestaccel:
            slowest.append(i)

    print "Slowest accel: %s" % (slowest,)

if args.p2:
    print "Doing part 2"

    states = {}
    for i in range(0,len(particles)):
        p = particles[i]
        states[i] = [p["p"],p["v"],p["a"],]

    iter = 0
    while True:
        if iter % 1000 == 0:
            print "Iter: %s" % (iter,)

        locs = {}
        collisions = set([])
        for key,state in states.items():
            pos = state[0]
            vel = state[1]
            acc = state[2]

            vel = (vel[0] + acc[0], vel[1] + acc[1], vel[2] + acc[2],)
            pos = (pos[0] + vel[0], pos[1] + vel[1], pos[2] + vel[2],)

            state[0] = pos
            state[1] = vel

            if pos in locs:
                locs[pos].append(key)
                collisions.add(pos)
            else:
                locs[pos] = [key,]

        if collisions:
            for collideloc in collisions:
                for collider in locs[collideloc]:
                    del states[collider]
            print "Iter: %s Collisions: %s Number of particles: %s" % (iter,len(collisions),len(states),)

        iter = iter + 1
