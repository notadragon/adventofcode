#!/usr/bin/env python

buttons=( (1,2,3), (4,5,6), (7,8,9), )

loc=(1,1)
deltas={}
deltas["U"] = (-1,0)
deltas["R"] = (0,1)
deltas["L"] = (0,-1)
deltas["D"] = (1,0)

for x in open("input"):
    x = x.strip()

    for c in x:
        d = deltas[c]
        newloc = (loc[0] + d[0], loc[1] + d[1],)


        if newloc[0] < 0 or newloc[0] > 2 or newloc[1] < 0 or newloc[1] > 2:
            newloc = loc

        #print "%s=%s . %s . %s=%s" % (loc,buttons[loc[0]][loc[1]],c,newloc,buttons[newloc[0]][newloc[1]],)
        
        loc = newloc


    print buttons[loc[0]][loc[1]]
