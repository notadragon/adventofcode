#!/usr/bin/env python

#f = open("11.data","r")
#serialno = int(f.readline().strip())
#serialno = 18
#serialno = 42
serialno = 7511
serialno = 9798
 
grid=[[0 for i in range(300)] for i in range(300)]
for x in range(300):
    for y in range(300):
        rackid = x + 11
        grid[x][y] = (((((y+1) * rackid + serialno) * rackid) // 100) % 10 ) - 5
 
maxpower = -9**9
maxloc = (0,0)
maxsize = 1
for x in range(0,300):
    for y in range(0, 300):
        power = grid[x][y]
        if power > maxpower:
            maxpower = power
            maxloc = (x+1, y+1)
            maxsize = 1
            print(maxpower, maxloc, maxsize)
        for s in range(2, min(301-x,301-y)):
            for i in range(0,s-1):
                power += grid[x+s-1][y+i] + grid[x+i][y+s-1]
            power += grid[x+s-1][y+s-1]
            if power > maxpower:
                maxpower = power
                maxloc = (x+1, y+1)
                maxsize = s
                print(maxpower, maxloc, maxsize)
 
print(maxpower, maxloc, maxsize)
