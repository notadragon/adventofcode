#!/usr/bin/env pypy

import argparse, re, itertools, collections

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

lineRe = re.compile("(Hit Points: (\d+))|(Damage: (\d+))|(Armor: (\d+)).*")

hp = None
damage = None
armor = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(2):
        hp = int(m.group(2))
    elif m.group(4):
        damage = int(m.group(4))
    elif m.group(6):
        armor = int(m.group(6))

print("HP: %s  Damage: %s  Armor: %s" % (hp,damage,armor,))

boss = (hp,damage,armor)

#Weapons:    Cost  Damage  Armor
#Dagger        8     4       0
#Shortsword   10     5       0
#Warhammer    25     6       0
#Longsword    40     7       0
#Greataxe     74     8       0

weapons = (
    ("Dagger",        8,     4,       0,),
    ("Shortsword",   10,     5,       0,),
    ("Warhammer",    25,     6,       0,),
    ("Longsword",    40,     7,       0,),
    ("Greataxe",     74,     8,       0,),
)

#Armor:      Cost  Damage  Armor
#Leather      13     0       1
#Chainmail    31     0       2
#Splintmail   53     0       3
#Bandedmail   75     0       4
#Platemail   102     0       5

armor = (
    ("Leather",      13,     0,       1,),
    ("Chainmail",    31,     0,       2,),
    ("Splintmail",   53,     0,       3,),
    ("Bandedmail",   75,     0,       4,),
    ("Platemail",   102,     0,       5,),
)


#Rings:      Cost  Damage  Armor
#Damage +1    25     1       0
#Damage +2    50     2       0
#Damage +3   100     3       0
#Defense +1   20     0       1
#Defense +2   40     0       2
#Defense +3   80     0       3

rings = (
    ("Damage +1",    25,     1,       0,),
    ("Damage +2",    50,     2,       0,),
    ("Damage +3",   100,     3,       0,),
    ("Defense +1",   20,     0,       1,),
    ("Defense +2",   40,     0,       2,),
    ("Defense +3",   80,     0,       3,),
)

def playgame( player, boss, equipment ):
    #print("Player: %s  Equipment: %s" % (player,equipment,))

    hp = player[0]
    damage = player[1] + sum([ e[2] for e in equipment])
    armor = player[2] + sum([ e[3] for e in equipment])

    bosshp = boss[0]
        
    while True:
        bosshp = bosshp - (max(0,damage - boss[2]))
        if bosshp <= 0:
            return True

        hp = hp - (max(0,boss[1] - armor))
        if hp <= 0:
            return False

if args.p1 or args.p2:
    print("Doing part 1 and 2")

    def genweapons():
        for w in weapons:
            yield (w,)

    def genarmor():
        yield ()
        for a in armor:
            yield (a,)

    def genrings():
        yield ()
        for r in rings:
            yield (r,)
        for rs in itertools.combinations(rings,2):
            yield rs

    if args.input == "input":
        myhp = 100
    else:
        myhp = 8
        
    bestwin = None
    bestwinner = None
    worstloss = None
    worstloser = None
    
    for w,a,r in itertools.product(genweapons(),genarmor(),genrings()):
        equipment = w + a + r
        result = playgame((100,0,0),boss,equipment)
        cost = sum([e[1] for e in equipment])

        if result:
            if bestwin == None or cost < bestwin:
                bestwin = cost
                bestwinner = equipment
                print("Best win: %s -> %s" % (bestwinner,bestwin,))
        else:
            if worstloss == None or worstloss < cost:
                worstloss = cost
                worstloser = equipment
                print("Worst loss: %s -> %s" % (worstloser,worstloss,))
            
    print("Best win (p1): %s -> %s" % (bestwinner,bestwin,))
    print("Worst loss (p2): %s -> %s" % (worstloser,worstloss,))
    
