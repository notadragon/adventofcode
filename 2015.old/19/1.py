#!/usr/bin/env python

import re, itertools

lineRe = re.compile("([A-Za-z][a-z]?) => (\w+)")
puzzleRe = re.compile("([A-Za-z][a-z]?)+")
mRe = re.compile("[A-Za-z][a-z]?")

mapping={}

puzzle = None

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if m:
        i=m.group(1)
        v=m.group(2)
        if mapping.has_key(i):
            mapping[i].append(v)
        else:
            mapping[i] = [v,]
        continue

    m = puzzleRe.match(line)
    if m:
        puzzle=line
        continue

    print "Invalid line: %s" % (line,)
    
print "Mapping:%s" % (mapping,)
print "Puzzle:%s" % (puzzle,)
        
def expand(inputVal,output):
    splitup = mRe.findall(inputVal)
    for i in range(0,len(splitup)):
        val = splitup[i]
        if mapping.has_key(val):
            for r in mapping[val]:
                repl = "".join(splitup[0:i] + [r,] + splitup[i+1:])
                output.add(repl)

possible = set()
expand(puzzle,possible)

print "Total replacements: %s" % (len(possible),)

#numIterations = 0
#vals = set()
#vals.add("e")
#
#while puzzle not in vals:
#    numIterations += 1
#
#    newvals = set()
#    for val in vals:
#        expand(val,newvals)
#    vals = newvals
#    print "Iteration: %s Vals: %s" % (numIterations,len(vals),)

reversemapping = {}
for i,vals in mapping.items():
    for v in vals:
        if reversemapping.has_key(v):
            reversemapping[v].append(i)
        else:
            reversemapping[v] = [i,]

reverseRe = re.compile("(" + "|".join(reversemapping.keys()) + ")")
valsize = max([len(x) for x in reversemapping.keys()])

def contract(inputval, existingvals, newvals):
    for i in range(0,min(20,len(inputval))):
        for v in range(0,valsize):
            ival = inputval[i:i+v]
            if reversemapping.has_key(ival):
                for r in reversemapping[ival]:
                    newval = inputval[0:i] + r + inputval[i+v:]
                    if newval not in existingvals:
                        existingvals.add(newval)
                        newvals.add(newval)

existingvals = set()
newvals = set()
existingvals.add(puzzle)
newvals.add(puzzle)
maxlen = len(puzzle) + 1

numiterations = 0
while "e" not in existingvals:
    existingvals=set()
    numiterations += 1

    prevmin = min([len(x) for x in newvals])
    prevvals = newvals
    newvals = set()

    expanded = 0
    for val in prevvals:
        if len(val) == prevmin:
            expanded += 1
            contract(val,existingvals,newvals)

    minlen = min([len(x) for x in newvals])
    maxlen = max([len(x) for x in newvals])
    print "Iteration: %s Found: %s Expanded: %s NewVals: %s Lens: %s->%s" % (numiterations,len(existingvals),expanded,len(newvals),minlen,maxlen,)
