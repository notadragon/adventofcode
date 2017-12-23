#!/usr/bin/env pypy

import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,nargs='?',default="input")
parser.add_argument("--p1",dest="p1",action='store_true')
parser.add_argument("--no-p1",dest="p1",action='store_false')
parser.add_argument("--p2",dest="p2",action='store_true')
parser.add_argument("--no-p2",dest="p2",action='store_false')

args = parser.parse_args()

if not args.p1 and not args.p2:
    args.p1 = True

print "Input: %s P1: %s p2: %s" % (args.input,args.p1,args.p2)

instructions = []
lineRe = re.compile("^(?:(setifprime|sub|jnz|snd|jgz|set|mod|add|mul|rcv) (-?[0-9]+|[a-z])(?: ([a-z]|-?[0-9]+))?)|(pass)(//.*)?$")
numberRe = re.compile("-?[0-9]+")

def parseval(arg):
    if not arg:
        return None
    m = numberRe.match(arg)
    if m:
        return int(arg)
    else:
        return arg
    
def getval(registers, reg):
    if isinstance(reg,int):
        output = reg
    elif not reg:
        output = None
    else:
        return registers.get(reg,0)
            
    #print "GetVal %s %s->%s" % (registers,reg,output)
    return output


hfl = { (("set","s",1),
         ("set","q",2),
         ("set","r",2),
         ("set","t","q"),
         ("mul","t","r"),
         ("sub","t","p"),
         ("jnz","t",2),
         ("set","s",0),
         ("sub","r",-1),
         ("set","t","r"),
         ("sub","t","p"), 
         ("jnz","t",-8),
         ("sub","q",-1),
         ("set","t","q"),
         ("sub","t","p"),
         ("jnz","t",-13),) : (("setifprime","s","p"),) }
        
def optimize(instrs):
    output = []

    i = 0
    while i < len(instrs):
        matched = False
        for unopt,opt in hfl.items():
            if i + len(unopt) > len(instrs):
                continue
            regmap = {}
            matched = True
            for j in range(0,len(unopt)):
                instr = instrs[i+j]
                uinstr = unopt[j]

                if instr[0] != uinstr[0]:
                    matched = False
                    break
                if len(instr) != len(uinstr):
                    matched = False
                    break
                for arg in range(1,len(instr)):
                    if isinstance(instr[arg],int) != isinstance(uinstr[arg],int):
                        matched = False
                        break
                    if instr[arg] == None:
                        if uinstr[arg] != None:
                            matched = False
                            break
                    elif isinstance(instr[arg],int):
                        if instr[arg] != uinstr[arg]:
                            matched = False
                            break
                    else:
                        if uinstr[arg] in regmap:
                            if instr[arg] != regmap[uinstr[arg]]:
                                matched = False
                                break
                        else:
                            regmap[uinstr[arg]] = instr[arg]
            if not matched:
                break
            if matched:
                for j in range(0,len(unopt)):
                    if j < len(opt):
                        oinstr = opt[j]
                        output.append( tuple(( regmap.get(x,x) for x in oinstr )) )
                    else:
                        output.append( None )
                i = i + len(unopt)
                break
        if not matched:
            output.append( instrs[i] )
            i = i + 1
                
    return output

for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        print "Invalid line: %s" % (x,)
        continue

    if not m.group(1):
        instructions.append(None)
    else:
        instr = m.group(1),parseval(m.group(2)),parseval(m.group(3))
        instructions.append(instr)

def isprime(x):
    y = 2
    while y*y < x:
        if x % y == 0:
            return 0
        y = y + 1
        
        
def runprog(cmdsrun,registers,inqueue):
    instr = 0

    while True:
        if instr < 0 or instr >= len(instructions):
            return

        if not instructions[instr]:
            instr = instr + 1
            continue
        
        cmd,reg,arg = instructions[instr]

        #print "Command: %s: (%s,%s,%4s) regs: %s" % (instr,cmd,reg,arg,registers,)
        
        cmdsrun[cmd] = cmdsrun.get(cmd,0) + 1

        if cmd == "setifprime":
            registers[reg] = isprime(getval(registers,arg))
        if cmd == "snd":
            yield getval(registers,reg)
        elif cmd == "set":
            registers[reg] = getval(registers,arg)
        elif cmd == "add":
            registers[reg] = getval(registers,reg) + getval(registers,arg)
        elif cmd == "sub":
            registers[reg] = getval(registers,reg) - getval(registers,arg)
        elif cmd == "mul":
            registers[reg] = getval(registers,reg) * getval(registers,arg)
        elif cmd == "mod":
            registers[reg] = getval(registers,reg) % getval(registers,arg)
        elif cmd == "rcv":
            if inqueue:
                registers[reg] = inqueue.pop(0)
            else:
                yield None
                continue
        elif cmd == "jnz":
            val = getval(registers,reg)
            if val != 0:
                instr = instr + getval(registers,arg)
                continue
        elif cmd == "jgz":
            val = getval(registers,reg)
            if val > 0:
                instr = instr + getval(registers,arg)
                continue
            
        instr = instr + 1
            
#for x in instructions:
#     print x

if args.p1:
    print "Doing part 1"

    cmdsrun = {}
    registers = {}
    queue = []
    r = runprog(cmdsrun,registers,queue)
    for x in r:
        pass
    print "Cmdsrun: %s" % (cmdsrun,)
    print "registers: %s" % (registers,)
    
if args.p2:
    print "Doing part 2"

    instructions = optimize(instructions)

    cmdsrun = {}
    registers = {"a":1}
    queue = []
    r = runprog(cmdsrun,registers,queue)
    for x in r:
        pass
    print "Cmdsrun: %s" % (cmdsrun,)
    print "registers: %s" % (registers,)
