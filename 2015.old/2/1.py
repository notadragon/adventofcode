#!/usr/bin/env python

total=0
totalribbon=0
for line in open("input").readlines():
    line=[ int(x) for x in line.split("x") ]

    area=2*(line[0] * line[1] + line[0]*line[2] + line[1]*line[2])
    slack=min(line[0]*line[1],line[0]*line[2],line[1]*line[2])

    ribbon1=2*min(line[0]+line[1],line[0]+line[2],line[1]+line[2])
    ribbon2=line[0]*line[1]*line[2]
    totalribbon=totalribbon+ribbon1+ribbon2
    
    print "Box: %s Area: %s Slack:%s Ribbon: %s+%s" % (line,area,slack,ribbon1,ribbon2,)
    total=total+area+slack
print "Total:%s Ribbon:%s" % (total,totalribbon)

