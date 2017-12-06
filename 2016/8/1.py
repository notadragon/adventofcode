#!/usr/bin/env python

import re, md5

screen=[]
for x in range(0,6):
    row=[]
    screen.append(row)
    for y in range(0,50):
        row.append(0)

rectRe = re.compile("rect ([0-9]+)x([0-9]+)")
rotateRe = re.compile("rotate (row y|column x)=([0-9]+) by ([0-9]+)")

for l in open("input").readlines():
    l = l.strip()

    m = rectRe.match(l)
    if m:
        x = int(m.group(1))
        y = int(m.group(2))
        for i in range(0,y):
            for j in range(0,x):
                screen[i][j] = 1
        continue

    m = rotateRe.match(l)
    if rotateRe:
        xy = m.group(1)[-1:]
        c = int(m.group(2))
        b = int(m.group(3))

        if xy == "y":
            b = b % 50
            row = screen[c]
            newrow = row[50-b:] + row[0:50-b]
            screen[c] = newrow
        else:
            b = b % 6
            col = []
            for i in range(0,6):
                col.append(screen[i][c])
            newcol = col[6-b:] + col[0:6-b]
            for i in range(0,6):
                screen[i][c] = newcol[i]
        continue
    print l

for row in screen:
    out=""
    for x in row:
        if x != 0:
            out = out + "#"
        else:
            out = out + "."
    print "%s" % (out,)

total = 0
for row in screen:
    for col in row:
        total = total + col

print total

        
