#!/usr/bin/env python

buttons=( ("X","X","1","X","X",),
          ("X","2","3","4","X",),
          ("5","6","7","8","9",),
          ("X","A","B","C","X",),
          ("X","X","D","X","X",),
          )

loc=(2,2)
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


        if newloc[0] < 0 or newloc[0] > 4 or newloc[1] < 0 or newloc[1] > 4 or buttons[newloc[0]][newloc[1]]=="X":
            newloc = loc

        #print "%s=%s . %s . %s=%s" % (loc,buttons[loc[0]][loc[1]],c,newloc,buttons[newloc[0]][newloc[1]],)
        
        loc = newloc


    print buttons[loc[0]][loc[1]]
