#!/usr/bin/env pypy3

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

lineRe = re.compile("^([a-z]+): (?:([0-9]+)|(?:([a-z]+) ([-+*/]) ([a-z]+))).*$")

data = []
for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line
    if m.group(2):
        data.append( ( m.group(1), int(m.group(2)), ) )
    else:
        data.append( ( m.group(1), m.group(3), m.group(4), m.group(5), ) )

#for d in data:
#    print(f"{d}")

def evalmonkey(monkeys, name):
    k = monkeys[name]
    if len(k) == 1:
        return k[0]
    elif len(k) == 3:
        m1 = evalmonkey(monkeys, k[0])
        m2 = evalmonkey(monkeys, k[2])

        if k[1] == "+":
            val = m1 + m2
        elif k[1] == "-":
            val = m1 - m2
        elif k[1] == "*":
            val = m1 * m2
        elif k[1] == "/":
            val = m1 // m2

        #print(f"{name} = {k[0]} {k[1]} {k[2]} = {m1} {k[1]} {m2} = {val}")
        monkeys[name] = (val,)
        return val
            

if args.p1:
    print("Doing part 1")

    monkeys = {}
    for d in data:
        monkeys[d[0]] = d[1:]

    val = evalmonkey(monkeys,"root")
    print(f"'root': {val}")

def printFormula(coefficients):
    output = []

    for i in range(0, len(coefficients)):
        power = len(coefficients) - i - 1
        if power == 0:
            output.append(f"{coefficients[i]}")
        elif power == 1:
            output.append(f"{coefficients[i]} * humn")
        else:
            output.append(f"{coefficients[i]} * humn^{power}")

    return " + ".join(output)

def mulcoeffs(lhs, rhs):
    output = []

    for lp in range(0,len(lhs)):
        lpc = lhs[-lp-1]
        for rp in range(0,len(rhs)):
            rpc = rhs[-rp-1]
            p = lp + rp
            while len(output) <= p+1:
                output.append(0)
            output[p] = output[p] + lpc*rpc
    output.reverse()
    return output    

def addcoeffs(lhs, rhs):
    output = []
    for i in range(0, max(len(lhs), len(rhs))):
        c = 0
        if i < len(lhs):
            c = c + lhs[-i-1]
        if i < len(rhs):
            c = c + rhs[-i-1]
        output.append(c)

    output.reverse()
    return output

class Formula:
    def __init__(self, *coefficients):
        self.coeffs = list(coefficients)
        self.invcoeffs = [1]


    def __repr__(self):
        if not self.coeffs:
            return "0"
        if self.invcoeffs == [1]:
            return printFormula(self.coeffs)
        else:
            return f"({printFormula(self.coeffs)}) / ({printFormula(self.invcoeffs)})"

    def normalize(self):
        while self.coeffs and self.coeffs[0] == 0:
            del self.coeffs[0]
        while self.invcoeffs and self.invcoeffs[0] == 0:
            del self.invcoeffs[0]
            
        
    def add(self, rhs):
        lhscoeffs = mulcoeffs(self.coeffs, rhs.invcoeffs)
        rhscoeffs = mulcoeffs(rhs.coeffs, self.invcoeffs)
        dencoeffs = mulcoeffs(self.invcoeffs, rhs.invcoeffs)
        output = Formula()
        output.coeffs = addcoeffs(lhscoeffs, rhscoeffs)
        output.invcoeffs = dencoeffs
        output.normalize()
        return output

    def sub(self, rhs):
        lhscoeffs = mulcoeffs(self.coeffs, rhs.invcoeffs)
        rhscoeffs = mulcoeffs(rhs.coeffs, self.invcoeffs)
        rhscoeffs = mulcoeffs(rhscoeffs, [-1])
        dencoeffs = mulcoeffs(self.invcoeffs, rhs.invcoeffs)
        output = Formula()
        output.coeffs = addcoeffs(lhscoeffs, rhscoeffs)
        output.invcoeffs = dencoeffs
        output.normalize()
        return output

    def mul(self, rhs):
        output = Formula()
        output.coeffs = mulcoeffs(self.coeffs, rhs.coeffs)
        output.invcoeffs = mulcoeffs(self.invcoeffs, rhs.invcoeffs)
        output.normalize()
        return output

    def div(self, rhs):
        output = Formula()
        output.coeffs = mulcoeffs(self.coeffs, rhs.invcoeffs)
        output.invcoeffs = mulcoeffs(self.invcoeffs, rhs.coeffs)
        output.normalize()
        return output

    def solve(self, rhs):
        lhscoeffs = mulcoeffs(self.coeffs, rhs.invcoeffs)
        rhscoeffs = mulcoeffs(rhs.coeffs, self.invcoeffs)
        rhscoeffs = mulcoeffs(rhscoeffs, [-1])

        output = Formula()
        output.coeffs = addcoeffs(lhscoeffs, rhscoeffs)
        output.normalize()
        return output

    def roots(self):
        if len(self.coeffs) > 2 or len(self.invcoeffs) > 1:
            return "NOPE"

        return (-self.coeffs[1]) // self.coeffs[0]
    
def evalmonkey2(monkeys, name):
    k = monkeys[name]
    if isinstance(k,Formula):
        return k
    elif len(k) == 1:
        val = Formula(k[0])
        #print(f"{name} {k} -> Formula")
        monkeys[name] = val
        return val
    elif len(k) == 3:
        m1 = evalmonkey2(monkeys, k[0])
        m2 = evalmonkey2(monkeys, k[2])

        if k[1] == "+":
            val = m1.add(m2)
        elif k[1] == "-":
            val = m1.sub(m2)
        elif k[1] == "*":
            val = m1.mul(m2)
        elif k[1] == "/":
            val = m1.div(m2)
        elif k[1] == "=":
            val = m1.solve(m2)

        #print(f"{name} = {k[0]} {k[1]} {k[2]} = {m1} {k[1]} {m2} = {val}")
        monkeys[name] = val
        return val
            
if args.p2:
    print("Doing part 2")

    monkeys = {}
    for d in data:
        monkeys[d[0]] = d[1:]

    monkeys["humn"] = Formula(1, 0)
    monkeys["root"] = ( monkeys["root"][0], "=", monkeys["root"][2], )

    val = evalmonkey2(monkeys,"root")
    print(f"{val} = 0")

    roots = val.roots()
    print(f"Roots: {roots}")
