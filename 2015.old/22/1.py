#!/usr/bin/env python

import re, itertools, math, sys

lineRe = re.compile("(.+): (\\d+)")

bossvals={}
myvals={"Hit Points":100,"Mana":500,}
    
for line in open("input").readlines():
    line = line.strip();
    if not line: continue

    m = lineRe.match(line)
    if not m:
        print "Invalid line: %s" % (line,)

    bossvals[m.group(1)] = int(m.group(2))

def mm(player,boss,output):
    if output: print "Player casts Magic Missile"
    player.spendMana(53)
    boss.hp -= 4


def drain(player,boss,output):
    if output: print "Player casts Drain"
    player.spendMana(73)
    player.hp += 2
    boss.hp -= 2


def shield(player,boss,output):
    if output: print "Player casts Shield"

    if player.shields:
        if output: print "Shield is already active"
        return
        
    player.spendMana(113)
    player.shields.append(6)
    player.armor += 7

def poison(player,boss,output):
    if output: print "Player casts Poison"

    if boss.poisons:
        if output: print "Poison is already active"
        return
        
    player.spendMana(173)
    boss.poisons.append(6)

def recharge(player,boss,output):
    if output: print "Player casts Recharge"
    if player.recharges:
        if output: print "Recharge is already active"
        return

    player.spendMana(229)
    player.recharges.append(5)

def bosshit(player,boss,output):
    parmor = player.armor
    battack = max(1,boss.damage-parmor)
    player.hp -= battack
    if output: print "Boss attacks for %s - %s = %s damage!" % (boss.damage,parmor,battack,)

allops={
    "mm":mm,
    "drain":drain,
    "shield":shield,
    "poison":poison,
    "recharge":recharge,
    }
    
class Boss:
    def __init__(self,hp,damage):
        self.hp = hp
        self.damage = damage
        self.poisons = []

class Player:
    def __init__(self,hp,mana):
        self.hp = hp
        self.armor = 0
        self.mana = mana
        self.manaspent = 0
        self.shields = []
        self.recharges = []

    def spendMana(self,amt):
        self.manaspent += amt
        self.mana -= amt
        
def run(b,p,ops,output, hard):

    turn = 0
    for opname in ops:
        op = allops[opname]
        
        turn += 1
        if output: print "-- Player turn %s --" % (turn,)
        if output: print "- Player has %s hit points, %s armor, %s mana" % (p.hp,p.armor,p.mana,)
        if output: print "- Boss has %s hit points" % (b.hp,)

        if hard:
            p.hp -= 1
            if p.hp <= 0:
                if output: print "Player has been killed by hard mode"
                return False
        
        for t in p.shields:
            if t == 1:
                p.armor -= 7
                if output: print "Shield wears off, decreasing armor by 7"
            else:
                if output: print "Shield's timer is now %s" % (t-1,)
                pass
        for t in b.poisons:
            if output: print "Poison deals %s damage; its timer is now %s" % (3,t-1,)
            b.hp -= 3
            if b.hp <= 0:
                if output: print "The Boss is dead from poison."
                return p.manaspent
        for t in p.recharges:
            if output: print "Recharges provides %s mana; its timer is now %s" % (101,t-1,)
            p.mana += 101
            
        p.shields = [x-1 for x in p.shields if x > 1]
        b.poisons = [x-1 for x in b.poisons if x > 1]
        p.recharges = [x-1 for x in p.recharges if x > 1]

        op(p,b,output)

        if p.mana < 0:
            if output: print "The player spent too much mana."
            return False
        if p.hp <= 0:
            if output: print "The player is dead."
            return False
        if b.hp <= 0:
            if output: print "The Boss is dead."
            return p.manaspent        

        if output: print 
        if output: print "-- Boss turn --"
        if output: print "- Player has %s hit points, %s armor, %s mana" % (p.hp,0+7*len(p.shields),p.mana,)
        if output: print "- Boss has %s hit points" % (b.hp,)
        for t in p.shields:
            if t == 1:
                p.armor -= 7
                if output: print "Shield wears off, decreasing armor by 7"
            else:
                if output: print "Shield's timer is now %s" % (t-1,)
                pass
        for t in b.poisons:
            if output: print "Poison deals %s damage; its timer is now %s" % (3,t-1,)
            b.hp -= 3
            if b.hp <= 0:
                if output: print "The Boss is dead from poison."
                return p.manaspent
        for t in p.recharges:
            if output: print "Recharges provides %s mana; its timer is now %s" % (101,t-1,)
            p.mana += 101
            
        bosshit(p,b,output)

        if p.mana < 0:
            if output: print "The player spent too much mana."
            return False
        if p.hp <= 0:
            if output: print "The player is dead."
            return False
        if b.hp <= 0:
            if output: print "The Boss is dead."
            return p.manaspent
        
        p.shields = [x-1 for x in p.shields if x > 1]        
        b.poisons = [x-1 for x in b.poisons if x > 1]
        p.recharges = [x-1 for x in p.recharges if x > 1]

        if output: print 
    if output: print "Out of operations"
    return -p.manaspent

#out = run( Boss(13,8), Player(10,250),(poison,mm,), True )
#print "Output was: %s" % (out,)

#out = run( Boss(14,8), Player(10,250), (recharge,shield,drain,poison,mm,), True)
#print "Output was: %s" % (out,)

#out = run( Boss(bossvals["Hit Points"],bossvals["Damage"]), Player(50,500),
#           ("shield","recharge","poison",
#            "shield","recharge","poison",
#            "shield","recharge","poison",
#            "shield","mm","poison",
#            "mm",),  True)
#print "Output was: %s" % (out,)

prevVals = set()
prevVals.add( () )

prunemana=True

if len(sys.argv) == 4:
    bossvals["Hit Points"] = int(sys.argv[1])
    bossvals["Damage"] = int(sys.argv[2])
    bossvals["Hard"] = bool(sys.argv[3])

hard = bool(bossvals.get("Hard","True"))
    
print "BossVals: %s" % (bossvals,)

minMana = -1
for time in itertools.count():
    print "Turns: %s" % (time,)

    print "Previous turn unterminated paths: %s" % (len(prevVals),)

    winners = 0
    losers = 0
    pruned = 0
    
    newVals = set()
    for prev in prevVals:
        for op in allops.keys():
            
            teffects = prev[-2:]
            if op == "shield" and op in teffects:
                continue
            if op == "recharge" and op in teffects:
                continue
            if op == "poison" and op in teffects:
                continue
            
            newops = prev + (op,)
            newout = run( Boss(bossvals["Hit Points"],bossvals["Damage"]), Player(50,500), newops, False, hard)

            #print "NewOps %s -> %s" % (newops,newout,)

            if newout == False:
                losers += 1
                continue

            elif newout < 0:
                if prunemana:
                    if minMana < 0 or minMana > -newout:
                        newVals.add(newops)
                    else:
                        pruned += 1
            else:
                if minMana < 0 or newout < minMana:
                    minMana = newout
                    print "Ops: %s  manaspent: %s" % (newops,newout,)
                winners += 1

    if pruned > 0:
        print "Pruned paths: %s" % (pruned,)            
    if losers > 0:
        print "Losing paths found: %s" % (losers,)
    if winners > 0:
        print "Winning paths found: %s" % (winners,)

    prevVals = newVals

    if not prevVals:
        break
