#!/usr/bin/env python

import re, itertools, math

lineRe = re.compile("(.+): (\\d+)")

bossvals={}
myvals={"Hit Points":100,"Damage":0,"Armor":0,}
    
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)

    bossvals[m.group(1)] = int(m.group(2))


shopdef="""Type Cost Damage Armor
Weapon Dagger 8 4 0
Weapon Shortsword 10 5 0
Weapon Warhammer 25 6 0
Weapon Longsword 40 7 0
Weapon Greataxe 74 8 0
Armor Leather 13 0 1
Armor Chainmail 31 0 2
Armor Splintmail 53 0 3
Armor Bandedmail 75 0 4
Armor Platemail 102 0 5
Ring Damage+1 25 1 0
Ring Damage+2 50 2 0
Ring Damage+3 100 3 0
Ring Defense+1 20 0 1
Ring Defense+2 40 0 2
Ring Defense+3 80 0 3
"""
weaponshop={}
armorshop={}
ringshop={}
for shopline in shopdef.split("\n")[1:]:
    if not shopline: continue
    itemvals = shopline.split(" ")
    if itemvals[0] == "Weapon":
        weaponshop[itemvals[1]] = {"Name":itemvals[1],"Type":itemvals[0],"Cost":int(itemvals[2]),"Damage":int(itemvals[3]),"Armor":int(itemvals[4]),}
    elif itemvals[0] == "Armor":
        armorshop[itemvals[1]] = {"Name":itemvals[1],"Type":itemvals[0],"Cost":int(itemvals[2]),"Damage":int(itemvals[3]),"Armor":int(itemvals[4]),}
    else:
        ringshop[itemvals[1]] = {"Name":itemvals[1],"Type":itemvals[0],"Cost":int(itemvals[2]),"Damage":int(itemvals[3]),"Armor":int(itemvals[4]),}
    
    
print "Weapons: %s" % (weaponshop,)
print "Armor: %s" % (armorshop,)
print "Rings: %s" % (ringshop,)
print "BossVals: %s" % (bossvals,)
print "MyVals: %s" % (myvals,)

def pickWeapons():
    for weapon in weaponshop.values():
        yield (weapon,)

def pickArmor():
    yield ()
    for armor in armorshop.values():
        yield (armor,)

def pickRings():
    avail = [x for x in ringshop.values()]
    yield ()

    for i in range(0,len(avail)):
        yield (avail[i],)
        for j in range(i+1,len(avail)):
            yield (avail[i],avail[j],)
        
        
def pickBuys():
    for weapon in pickWeapons():
        for armor in pickArmor():
            for rings in pickRings():
                yield weapon + armor + rings


def wins(bossvals,myvals,items):
    mydamage = myvals["Damage"] + sum([x["Damage"] for x in items])
    mydef = myvals["Armor"] + sum([x["Armor"] for x in items])

    myhp = myvals["Hit Points"]

    bossdamage = bossvals["Damage"]
    bossdef = bossvals["Armor"]
    bosshp = bossvals["Hit Points"]

    while True:
        bosshp -= max(1,mydamage - bossdef)
        if bosshp <= 0:
            return True
        myhp -= max(1,bossdamage - mydef)
        if myhp <= 0:
            return False

mincost = -1
minbuy = None

maxcost = -1
maxbuy = None

for tobuy in pickBuys():
    cost = sum([x["Cost"] for x in tobuy])
    if wins(bossvals,myvals,tobuy):
        if mincost < 0 or cost < mincost:
            mincost = cost
            minbuy = tobuy
            print "WIN Tobuy: %s Cost: %s" % (tobuy,cost,)
    else:
        if cost > maxcost:
            maxcost = cost
            maxbuy = tobuy
            print "LOSE Tobuy: %s Cost: %s" % (tobuy,cost,)


print "Best Win: %s Cost %s" % (minbuy,mincost,)
print "Worst Loss: %s Cost %s" % (maxbuy,maxcost,)
