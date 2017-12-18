#!/usr/bin/env python

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
lineRe = re.compile("^(snd|jgz|set|mod|add|mul|rcv) (-?[0-9]+|[a-z])(?: ([a-z]|-?[0-9]+))?$")
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
    

for x in open(args.input).readlines():
    x = x.strip()

    m = lineRe.match(x)
    if not m:
        #print "Invalid line: %s" % (x,)
        continue

    instr = m.group(1),parseval(m.group(2)),parseval(m.group(3))
    instructions.append(instr)
    print "Instr %s -> %s" % (x,instr,)


if args.p1:
    print "Doing part 1"

    registers = {}

    lastsound = 0

    instr = 0
    while True:
        if instr < 0 or instr >= len(instructions):
            break
        
        cmd,reg,arg = instructions[instr]

        print "Command: %s: (%s,%s,%s) regs: %s" % (instr,cmd,reg,arg,registers,)
        
        if cmd == "snd":
            lastsound = getval(registers,reg)
            print "Play sound:%s" % (lastsound,)
        elif cmd == "set":
            registers[reg] = getval(registers,arg)
        elif cmd == "add":
            registers[reg] = getval(registers,reg) + getval(registers,arg)
        elif cmd == "mul":
            registers[reg] = getval(registers,reg) * getval(registers,arg)
        elif cmd == "mod":
            registers[reg] = getval(registers,reg) % getval(registers,arg)
        elif cmd == "rcv":
            if lastsound != 0:
                print "recovering sound %s" % (lastsound,)
                registers[reg] = lastsound
                break
        elif cmd == "jgz":
            val = getval(registers,reg)
            if val > 0:
                instr = instr + getval(registers,arg)
                continue

        instr = instr + 1
        
if args.p2:
    print "Doing part 2"

    def runprog(id,inqueue):
        registers = {"p":id,}
        instr = 0

        while True:
            if instr < 0 or instr >= len(instructions):
                return
        
            cmd,reg,arg = instructions[instr]

            #print "Command[%s]: %s: (%s,%s,%s) regs: %s" % (id,instr,cmd,reg,arg,registers,)
        
            if cmd == "snd":
                yield getval(registers,reg)
            elif cmd == "set":
                registers[reg] = getval(registers,arg)
            elif cmd == "add":
                registers[reg] = getval(registers,reg) + getval(registers,arg)
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
            elif cmd == "jgz":
                val = getval(registers,reg)
                if val > 0:
                    instr = instr + getval(registers,arg)
                    continue

            instr = instr + 1
            
    aqueue = []
    a = runprog(0,aqueue)
    bqueue = []
    b = runprog(1,bqueue)

    totalasent = 0
    totalbsent = 0
    while True:
        asent = 0
        bsent = 0
        for sent in a:
            print "A sent %s" % (sent,)
            if sent != None:
                asent = asent + 1
                totalasent = totalasent + 1
                bqueue.append(sent)
            else:
                break
        for sent in b:
            print "B sent %s" % (sent,)
            if sent != None:
                bsent = bsent + 1
                totalbsent = totalbsent + 1
                aqueue.append(sent)
            else:
                break

        if not asent and not bsent:
            break

    print "Totals sent: a:%s b:%s" % (totalasent,totalbsent,)
