#!/usr/bin/env python

import re, md5

lineRe = re.compile("/dev/grid/node-x([0-9]+)-y([0-9]+) +([0-9]+)T +([0-9]+)T +([0-9]+)T +([0-9]+)%")

nodes={}

for l in open("input").readlines()[2:]:
    l = l.strip()
    m = lineRe.match(l)
    if m:
        x=int(m.group(1))
        y=int(m.group(2))
        size=int(m.group(3))
        used=int(m.group(4))
        avail=int(m.group(5))
        usedpct=int(m.group(6))
        nodes[ (x,y) ] = [x,y,used,size,False]
        continue
    print l

viable = 0

minx=0
maxx=0
miny=0
maxy=0
for a in nodes.values():
    minx = min(a[0],minx)
    miny = min(a[1],miny)
    maxx = max(a[0],maxx)
    maxy = max(a[1],maxy)

print "Range: %s -> %s" % ( (minx,miny,), (maxx,maxy,))

nodes[ (maxx,0) ][4]=True

def show():
    for y in range(miny,maxy+1):
        l=[]
        for x in range(minx,maxx+1):
            n=nodes[(x,y)]
            if not n:
                l.append("    ")
            else:
                l.append("%s/%s%s" % (n[2],n[3],"!" if n[4] else "",))
                
        print " ".join(l)

def move(nodes,x,y,dx,dy):
    if not nodes.has_key( (x,y) ): return None
    if not nodes.has_key( (x+dx,y+dy) ): return None

    f=nodes[(x,y)][:]
    t=nodes[(x+dx,y+dy)][:]

    if f[4]:
        if t[2] > 0:
            return None
        f[4]=False
        t[4]=True
    
    d=f[2]
    if d == 0:
        return None
    
    f[2]=0

    t[2]=t[2]+d
    if t[2] > t[3]:
        return None
    
    outnodes=nodes.copy()
    outnodes[(x,y)]=f
    outnodes[(x+dx,y+dy)]=t

    return outnodes

step=0
done=False
states=[nodes,]
datapos=maxx

while True:
    print "step: %s" % (step,)
    print "States: %s" % (len(states,))
    print "datapos: %s" % (datapos,)
    
    if datapos == 0:
        print "Done"
        break
    
    newstates = []
    for nodes in states:
        datanode=nodes[(datapos,0)]

        nextnodes=move(nodes,datapos,0,-1,0)
        if nextnodes:
            newstates.append(nextnodes)

    if newstates:
        print "Data moved! %s -> %s" % (datapos,datapos-1,)
        
        datapos = datapos - 1
    else:
        for nodes in states:
            for y in range(miny,maxy+1):
                for x in range(minx,maxx+1):
                    node=nodes[(x,y)]
                    if node[4]:
                        continue
                    else:
                        deltas=[ (1,0), (0,1), (-1,0), (0,-1) ]
                        for dx,dy in deltas:
                            nextnodes = move(nodes,x,y,dx,dy)
                            if nextnodes:
                                newstates.append(nextnodes)

    states=newstates
    step=step+1

    if not states:
        break
        
