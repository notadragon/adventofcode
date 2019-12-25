#!/usr/bin/env pypy

import argparse, re, itertools, collections, heapq

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True
    args.p2 = True

print("Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2))

lineRe = re.compile("(Hit Points: (\d+))|(Damage: (\d+))|(hp: (\d+))|(mana: (\d+))|(missile|drain|shield|poison|recharge)")

bosshp = None
bossdamage = None

hp = 50
mana = 500

spells = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(2):
        bosshp = int(m.group(2))
    elif m.group(4):
        bossdamage = int(m.group(4))
    elif m.group(6):
        hp = int(m.group(6))
    elif m.group(8):
        mana = int(m.group(8))
    elif m.group(9):
        spells.append(m.group(9))

print("HP: %s Damage: %s" % (bosshp,bossdamage,))

actions = [
    ( "missile",  53, ),
    ( "drain",    73, ),
    ( "shield",   113, ),
    ( "poison",   173, ),
    ( "recharge", 229, ),
    ( "lose",     0, ),
]

def act(s):
    for a in actions:
        if a[0] == s:
            return a
    return None

initState = {
    "hp" : hp,
    "mana" : mana,
    "armor" : 0,
    "spentmana" : 0,
    "bosshp" : bosshp,
    "bossdamage" : bossdamage,
    }

def availableActions(state):
    mana = state["mana"]

    for a in actions:
        if mana < a[1]:
            continue
        if a[0] in state and state[a[0]] > 1:
            continue
        yield a

def damageboss(state,d):
    hp = state["bosshp"]
    hp = hp - d
    state["bosshp"] = hp
    if hp <= 0:
        state["done"] = "W"

def damageplayer(state,d):
    hp = state["hp"]
    hp = hp - d
    state["hp"] = hp
    if hp <= 0:
        state["done"] = "L"

def spendmana(state,m):
    state["mana"] = state["mana"] - m
    state["spentmana"] = state["spentmana"] + m

    if state["mana"] < 0:
        raise("Spent too much mana!")
    
def applyeffects(state,v):
    shieldturns = state.get("shield",0) - 1
    if v and shieldturns >= 0:
        print("Shield's timer is now %s." % (shieldturns,))
    if shieldturns > 0:
        state["shield"] = shieldturns 
    elif shieldturns == 0:
        del state["shield"]
        state["armor"] = state["armor"] - 7
        if v:
            print("Shield wears off, decreasing armor by 7.")
            
    poisonturns = state.get("poison",0)
    poisonturns = poisonturns - 1
    if poisonturns >= 0:
        if v:
            print("Poison deals %s damage; its timer is now %s." % (3,poisonturns,))
        damageboss(state,3)
    if poisonturns > 0:
        state["poison"] = poisonturns
    elif poisonturns == 0:
        del state["poison"]
        if v:
            print("poison wears off.")
            
    rechargeturns = state.get("recharge",0)
    rechargeturns = rechargeturns - 1
    if rechargeturns >= 0:
        if v:
            print("Recharge provides %s mana its timer is now %s." % (101,rechargeturns,))
        state["mana"] = state["mana"] + 101
    if rechargeturns > 0:
        state["recharge"] = rechargeturns
    elif rechargeturns == 0:
        del state["recharge"]        
        if v:
            print("Recharge wears off.")
        
def turn(state,action,v=False):
    output = state.copy()

    if v:
        print("")
        print("-- Player turn --")
        print("- Player has %s hit points, %s armor, %s mana" % (output["hp"], output["armor"], output["mana"], ) )
        print("- Boss has %s hit points" % (output["bosshp"],))

    if "hard" in state:
        damageplayer(output,1)

        if "done" in output:
            return output
        
    applyeffects(output,v)
    if "done" in output:
        return output

    spendmana(output,action[1])
    if action[0] == "missile":
        damageboss(output,4)
        if v:
            print("Player casts Magic Missile, dealing %s damage" % (4,))
    elif action[0] == "drain":
        damageboss(output,2)
        damageplayer(output,-2)
        if v:
            print("Player casts Drain, dealing %s damage, and healing %s hit points." % (2,2,))
    elif action[0] == "shield":
        output["shield"] = 6
        output["armor"] = output["armor"] + 7
        if v:
            print("Player casts Shield, increasing armor by %s." % (7,))
    elif action[0] == "poison":
        output["poison"] = 6
        if v:
            print("Player casts Poison.")
    elif action[0] == "recharge":
        output["recharge"] = 5
        if v:
            print("Player casts Recharge.")          
    elif action[0] == "lose":
        output["done"] = "L"
        if v:
            print("Player loses.")
            
    if "done" in output:
        return output

    if v:
        print("")
        print("-- Boss turn --")
        print("- Player has %s hit points, %s armor, %s mana" % (output["hp"], output["armor"], output["mana"], ) )
        print("- Boss has %s hit points" % (output["bosshp"],))
    
    applyeffects(output,v)
    if "done" in output:
        return output

    armor = output["armor"]

    bdamage = max(1,output["bossdamage"] - armor)
    damageplayer(output,bdamage)
    if v:
        if armor > 0:
            print("Boss attacks for %s - %s = %s damage." % (output["bossdamage"],armor,bdamage,))
        else:
            print("Boss attacks for %s damage." % (bdamage,))

    if "done" in output:
        return output

    return output

def findcheapest(initState):
    steps = [ (0, initState.copy(), ) ]

    steps[0][1]["actions"] = ()
        
    displayed = 0
    while steps:
        spent,gstate = heapq.heappop(steps)

        #print("gstate: %s" % (gstate,))

        if "done" in gstate:
            print("Winner: %s" % (gstate,))
            break

        if spent / 100 > displayed:
            displayed = spent / 100
            print("Spent Mana: %s" % (spent,))
        
        for action in availableActions(gstate):
            nstate = turn(gstate, action)
            if "done" in nstate and nstate["done"] == "L":
                continue
            nstate["actions"] = nstate["actions"] + (action[0],)
            heapq.heappush( steps, (nstate["spentmana"], nstate,) )

if args.p1:
    print("Doing part 1")

    if spells:
        state = initState.copy()
        for spell in spells:
            state = turn(state,act(spell),True)
        print("")
        print("Final State: %s" % (state,))

    else:
        findcheapest(initState)
        
        
if args.p2:
    print("Doing part 2")

    hinitState = initState.copy()
    hinitState["hard"] = True

    findcheapest(hinitState)
    
