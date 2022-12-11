#!/usr/bin/env pypy3

import argparse, re, itertools, collections, math

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

monkeys = {}

class Monkey:
    def __init__(self,num):
        self.num = num
        self.items = []
        self.op = ()
        self.test = ()
        self.conds = {}
        self.inspections = 0


def copyMonkey(m):
    output = Monkey(m.num)
    output.items = list(m.items)
    output.op = m.op
    output.test = m.test
    output.conds = m.conds.copy()
    output.inspections = m.inspections
    return output

def copyMonkeys(monkeys):
    return { k : copyMonkey(m) for k,m in monkeys.items() }
    
    
        
monkeyRe = re.compile("^Monkey ([0-9]+):$")
startingRe = re.compile("^Starting items: ([0-9, ]+)$")
opsRe = re.compile("^Operation: new = old (\+|\*) (?:([0-9]+)|(old))$")
testRe = re.compile("^Test: divisible by ([0-9]+)$")
condRe = re.compile("^If (true|false): throw to monkey ([0-9]+)$")

currMoneky = None

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    # Process input line
    m = monkeyRe.match(x)
    if m:
        currMonkey = Monkey(int(m.group(1)))
        monkeys[currMonkey.num] = currMonkey
        continue
    m = startingRe.match(x)
    if m:
        currMonkey.items = [ int(i) for i in m.group(1).split(",") ]
        continue
    m = opsRe.match(x)
    if m:
        if m.group(2):
            currMonkey.op = ( "new", "old", m.group(1), int(m.group(2)), )
        else:
            currMonkey.op = ( "new", "old", m.group(1), m.group(3), )
        continue
    m = testRe.match(x)
    if m:
        currMonkey.test = ( "div", int(m.group(1)), )
        continue
    m = condRe.match(x)
    if m:
        c = True if m.group(1) == "true"  else False
        currMonkey.conds[ c ] = ( "throw", int(m.group(2)), )
        continue
    
    print("Invalid line: %s" % (x,))

def applyOp(op, val, verbose = False):
    output = None
    if op[0] == "new":
        if op[1] == "old":
            if op[2] == "+":
                if op[3] == "old":
                    output = val + val
                    if verbose:
                        print(f"    Worry level is multiplied by itself to {output}")
                else:
                    output = val + op[3]
                    if verbose:
                        print(f"    Worry level is multiplied by {op[2]} to {output}")
            elif op[2] == "*":
                if op[3] == "old":
                    output = val * val
                    if verbose:
                        print(f"    Worry level is increased by itself to {output}")
                else:
                    output = val * op[3]
                    if verbose:
                        print(f"    Worry level increases by {op[2]} to {output}")
    if not output:
        print(f"    Unkonwn ops: {op}")
    return output
            

def dotest(test, val, verbose):
    if test[0] == "div":
        if (val % test[1]) == 0:
            if verbose:
                print(f"    Current worry level is divisible by {test[1]}")
            return True
        else:
            if verbose:
                print(f"    Current worry level is not divisible by {test[1]}")
            return False
    print(f"    Unkonwn test: {test}")
    return None

def applyCond(cond, monkeys, item, verbose = False):
    if cond[0] == "throw":
        monkeys[cond[1]].items.append(item)
        if verbose:
            print(f"    Item with worry level {item} is thrown to monkey {cond[1]}.")
    
def taketurn(monkey, monkeys, lcm, worried, verbose = False):
    if verbose:
        print(f"Monkey {monkey.num}:")
    tomove = monkey.items
    monkey.items = []
    for w in tomove:
        if verbose:
            print(f"  Monkey inspects an item with worry level of {w}")
        w = applyOp(monkey.op, w, verbose)

        if not worried:
            w  = w // 3
            if verbose:
                print(f"    Monkey gets bored with item.  WOrry level is divided by 3 to {w}")

        if verbose and (w != w % lcm):
            print(f"    Reducing worry mod {lcm} to {w % lcm}")
        w = w % lcm
                
        monkey.inspections = monkey.inspections + 1
        if dotest(monkey.test, w, verbose):
            applyCond(monkey.conds[True], monkeys, w, verbose)
        else:
            applyCond(monkey.conds[False], monkeys, w, verbose)

def showmonkeys(monkeys):
    for mnum in sorted(monkeys.keys()):
        m = monkeys[mnum]
        idesc = ", ".join([str(item) for item in m.items])
        print(f"Monkey {mnum}: {idesc}")

def showinspections(monkeys):
    for mnum in sorted(monkeys.keys()):
        m = monkeys[mnum]
        print(f"Monkey {mnum} inspected items {m.inspections} times.")
            
def takeround(monkeys, lcm, worried, verbose=False):
    for mnum in sorted(monkeys.keys()):
        taketurn(monkeys[mnum], monkeys, lcm, worried)
    if verbose:
        showmonkeys(monkeys)
        showinspections(monkeys)

def mb(monkeys):
    inspections = [ m.inspections for m in monkeys.values() ]
    inspections.sort()
    monkeybusiness = inspections[-2] * inspections[-1]    
    return monkeybusiness

if args.p1:
    print("Doing part 1")

    p1monkeys = copyMonkeys(monkeys)

    lcm = 1
    for m in p1monkeys.values():
        lcm *= m.test[1]


    for r in range(0,20):
        takeround(p1monkeys, lcm, False)
        #print(f"After round {r+1}, the monkeys are holding items with these worry levels:")
        #showmonkeys(p1monkeys)
        #showinspections(p1monkeys)

    monkeybusiness = mb(p1monkeys)
    print(f"Monkey Business: {monkeybusiness}")
    
if args.p2:
    print("Doing part 2")

    p2monkeys = copyMonkeys(monkeys)

    lcm = 1
    for m in p2monkeys.values():
        lcm *= m.test[1]

    for r in range(0,10000):
        takeround(p2monkeys, lcm, True)

        #if (r+1) in (1,20,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000):
            #print(f"== After round {r+1} ==")
            #showinspections(p2monkeys)
            
    monkeybusiness = mb(p2monkeys)
    print(f"Monkey Business: {monkeybusiness}")
