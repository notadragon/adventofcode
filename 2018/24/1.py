#!/usr/bin/env pypy

import argparse, re, itertools

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

lineRe = re.compile("(Immune System:)|(Infection:)|(?:([0-9]+) units each with ([0-9]+) hit points (?:\\((.*)\\) )?with an attack that does ([0-9]+) ([a-z]+) damage at initiative ([0-9]+))")
defRe = re.compile("(weak|immune) to ([a-z, ]+)")

groups = [[],[]]
dtypes = set()

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        continue
    
    # Process input line
    if m.group(1):
        group = groups[0]
    elif m.group(2):
        group = groups[1]
    else:
        numunits = int(m.group(3))
        hp = int(m.group(4))

        defenses = m.group(5)
        itypes = []
        wtypes = []
        if defenses:
            for d in defRe.findall(defenses):
                if d[0] == "weak":
                    wtypes.extend(d[1].split(", "))
                elif d[0] == "immune":
                    itypes.extend(d[1].split(", "))
                    
        damage = int(m.group(6))
        dtype = m.group(7)
        initiative = int(m.group(8))

        group.append( (numunits,hp,itypes,wtypes,damage,dtype,initiative) )

#print("Immune System:")
#for u in groups[0]:
#    print("  %s" % (u,))
            
#print("Infections:")
#for u in groups[1]:
#    print("  %s" % (u,))

class Unit:
    def __init__(self,a,n,u):
        self.army = a
        self.num = n
        self.numunits = u[0]
        self.hp = u[1]
        self.itypes = u[2]
        self.wtypes = u[3]
        self.damage = u[4]
        self.dtype = u[5]
        self.initiative = u[6]

        self.targetting = None
        self.targettedby = None
        
    def show(self):
        print("Group %s contains %s units (hp: %s d: %s(%s) i: %s wk: %s imm: %s epower:%s)" % (self.num, self.numunits, self.hp, self.damage, self.dtype, self.initiative, ",".join(self.wtypes), ",".join(self.itypes),self.effpower(),))

    def effpower(self):
        return self.numunits * self.damage

    def selecttarget(self):
        target = None
        tdamage = None
        for u in self.army.enemy.units:
            if u.targettedby:
                continue
            damage = self.damageto(u)
            if damage == 0:
                continue
            if not target:
                target = u
                tdamage = damage
                continue
            if damage > tdamage:
                target = u
                tdamage = damage
                continue
            if damage < tdamage:
                continue
            if u.effpower() > target.effpower():
                target = u
                tdamage = damage
                continue
            if u.effpower() < target.effpower():
                continue
            if u.initiative > target.initiative:
                target = u
                tdamage = damage
                continue
            if u.initiative < target.initiative:
                continue
            target = u
            tdamage = damage
        self.targetting = target
        if target:
            target.targettedby = self

    def damageto(self,u):
        if self.dtype in u.itypes:
            return 0
        elif self.dtype in u.wtypes:
            return 2 * self.damage * self.numunits
        else:
            return self.damage * self.numunits
        
class Army:
    def __init__(self,n,g):
        self.num = n
        self.units = [ Unit(self,n+1,u) for n,u in enumerate(g) ]

    def show(self):
        print("%s:" % (self.name,))
        for u in self.units:
            u.show()

    def rounddone(self):
        self.units = [u for u in self.units if u.numunits > 0 ]
        for u in self.units:
            u.targetting = None
            u.targettedby = None
            
class War:
    def __init__(self,groups):
        self.armies = [ Army(n+1,g) for n,g in enumerate(groups) ]

        self.armies[0].enemy = self.armies[1]
        self.armies[0].name = "Immune System"
        self.armies[1].enemy = self.armies[0]
        self.armies[1].name = "Infection"
        
    def show(self):
        self.armies[0].show()
        self.armies[1].show()

    def winner(self):
        if not self.armies[0].units:
            return self.armies[1]
        elif not self.armies[1].units:
            return self.armies[0]
        else:
            return None

    def rounddone(self):
        for a in self.armies:
            a.rounddone()

def dowar(boost):
    w = War(groups)

    verbose = False
    
    if verbose:
        w.show()
        print("")

    if boost:
        for u in w.armies[0].units:
            u.damage += boost
        
    round = 1
    while not w.winner():
        targetters = []

        if verbose:
            print("Round: %s" % (round,))
            w.show()
        
        for a in w.armies:
            for u in a.units:
                targetters.append( (-u.effpower(), -u.initiative, u,) )

        targetters.sort()
        attackers = []
        
        for epower,initiative,u in targetters:
            u.selecttarget()

            if u.targetting:
                if verbose:
                    print("%s group %s would deal defending group %s %s damage" % (u.army.name,u.num,u.targetting.num,u.damageto(u.targetting)))

                attackers.append( (-u.initiative, u,) )
            else:
                if verbose:
                    print("%s group %s would not attack" % (u.army.name,u.num,))
                pass
            
        attackers.sort()
        if verbose:
            print("")

        killed = 0
        for initiative,u in attackers:
            adamage = u.damageto(u.targetting)
            akill = min(u.targetting.numunits,adamage // u.targetting.hp)

            if verbose:
                print("%s group %s attacks defending group %s, killing %s units" % (u.army.name,u.num,u.targetting.num,akill,))

            u.targetting.numunits -= akill

            killed += akill

        w.rounddone()

        round = round + 1

        if killed == 0:
            return ("",-1)
            break
        
    warmy = w.winner()
    if verbose:
        print("Winner: %s" % (warmy.name,))
        print("Winning Units: %s" % (sum([u.numunits for u in warmy.units]),))
    return (warmy.name,sum([u.numunits for u in warmy.units]),)

if args.p1:
    print("Doing part 1")

    winner,winunits = dowar(0)
    print("Winner: %s" % (winner,))
    print("Winning Units: %s" % (winunits,))
    
if args.p2:
    print("Doing part 2")

    boost = 1
    while True:
        winner,winunits = dowar(boost)
        if winner == "Immune System":
            print("Boost: %s" % (boost,))
            print("Winner: %s" % (winner,))
            print("Winning Units: %s" % (winunits,))
            break
        boost = boost + 1
