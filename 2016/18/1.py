#!/usr/bin/env python

import re, md5


data = open("input").readlines()[0].strip()
print data

def nextrow(row):
    output = []
    for i in range(0,len(row)):
        if i == 0:
            l = "."
        else:
            l = row[i-1]
        c = row[i]
        if i == len(row)-1:
            r = "."
        else:
            r = row[i+1]

        if l == "^" and c == "^" and r == ".":
            t = "^"
        elif c == "^" and r == "^" and l == ".":
            t = "^"
        elif l == "^" and c == "." and r == ".":
            t = "^"
        elif r == "^" and c == "." and l == ".":
            t = "^"
        else:
            t = "."
        output.append(t)

    return "".join(output)

rows = [data,]
while len(rows) < 400000:
    rows.append(nextrow(rows[-1]))

total = 0
for r in rows:
    for x in r:
        if x == ".":
            total += 1

print total
    
