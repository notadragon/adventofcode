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

minsize =500
for n in nodes.values():
    minsize = min(minsize,n[3])

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

def viable(nodes,A,B):
    if not nodes.has_key(A): return False
    if not nodes.has_key(B): return False
    a = nodes[A]
    b = nodes[B]
    if a[0] == b[0] and a[1] == b[1]:
        return False
    if a[2] == 0:
        return False
    if a[2] + b[2] > b[3]:
        return False
    if a[4] and b[3] != 0:
        return False
    if b[4]:
        return False
    return True

def show2(nodes):
    for y in range(miny,maxy+1):
        l=[]
        for x in range(minx,maxx+1):
            n=nodes[(x,y)]
            if not n:
                l.append(" ")
            elif n[2] == 0:
                l.append("_")
            elif n[4]:
                l.append("D")
            elif n[2]<=minsize:
                l.append(".")
            else:
                l.append("#")
                
        print "".join(l)


def show(nodes):
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

allsteps = [(24,25,0,1),
            (24,24,0,1),]

for x in range(0,6):
    allsteps.append( (allsteps[-1][0]-1,allsteps[-1][1],1,0) )

for x in range(0,24):
    allsteps.append( (allsteps[-1][0],allsteps[-1][1]-1,0,1) )

for x in range(0,13):
    allsteps.append( (allsteps[-1][0]+1,allsteps[-1][1],-1,0) )

for x in range(0,30):
    allsteps.append( (allsteps[-1][0],allsteps[-1][1]+1,0,-1) )
    allsteps.append( (allsteps[-1][0]-1,allsteps[-1][1],1,0) )
    allsteps.append( (allsteps[-1][0]-1,allsteps[-1][1],1,0) )
    allsteps.append( (allsteps[-1][0],allsteps[-1][1]-1,0,1) )
    allsteps.append( (allsteps[-1][0]+1,allsteps[-1][1],-1,0) )
    
for x,y,dx,dy in allsteps:
    nodes = move(nodes,x,y,dx,dy)
    step = step + 1
    print "STEP[%s] = %s" % (step,(x,y,dx,dy,),) 

show2(nodes)
for y in range(miny,maxy+1):
    for x in range(minx,maxx+1):
        if nodes[ (x,y) ][4]:
            print "  Data:%s" % ( (x,y), )
        for dx,dy in [ (-1,0), (1,0), (0,-1), (0,1) ] :
            if viable(nodes,(x,y),(x+dx,y+dy)):
                print "  %s -> %s (%s)" % ( (x,y), (x+dx,y+dy), (dx,dy), )
print "Steps:%s" % (step,)                
