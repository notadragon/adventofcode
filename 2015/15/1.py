#!/usr/bin/env python

import re, itertools

lineRe = re.compile("(\\w.*): capacity (-?\\d+), durability (-?\\d+), flavor (-?\\d+), texture (-?\\d+), calories (-?\\d+)")

vals = {}

for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)
        continue
    
    name=m.group(1)
    capacity = int(m.group(2))
    durability = int(m.group(3))
    flavor = int(m.group(4))
    texture = int(m.group(5))
    calories = int(m.group(6))

    vals[name] = [capacity,durability,flavor,texture,calories]
    
def getScore(ingredients):
    output = 0

    totals=[0,0,0,0]
    for name,count in ingredients:
        ivals = vals[name]
        for i in range(0,4):
            totals[i] = totals[i] + ivals[i]*count
        
    return reduce(lambda x,y: max(x,0)*max(y,0), totals)

def getCalories(ingredients):
    out = 0
    for name,count in ingredients:
        out += vals[name][4] * count
    return out

def getIngredients(names,count):
    name = names[0]
    othernames = names[1:]

    if not othernames:
        yield ( (name,count), )
    
    for i in range(0,count+1):
        if i > 0:
            out = ( (name,i), )
        else:
            out = ()
        
        if count > i and othernames:
            for rest in getIngredients(othernames,count-i):
                yield out + rest

#print getScore((('Butterscotch', 0), ('Sprinkles', 50), ('Candy', 50)))


best = None
bestScore = 0
for ingredients in getIngredients(vals.keys(),100):
    cals = getCalories(ingredients)
    if cals != 500:
        continue

    score = getScore(ingredients)
    if not best or score > bestScore:
        best = ingredients
        bestScore = score

        print "Best: %s -> cals:%s score:%s" % (ingredients, cals, score, )
        
