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

lineRe = re.compile(".*")

commands = []

for x in open(args.input).readlines():
    x = x.strip()
    if not x:
        continue

    m = lineRe.match(x)
    if not m:
        print("Invalid line: %s" % (x,))
        
    # Process input line

    if x.startswith("$"):
        newcommand = x.split(" ")[1:]
        commands.append( [ newcommand,])
    else:
        commands[-1].append(x.split(" "))

#for c in commands:
#    print(f"{c}")

def showdir(dirs, p):
    if p in dirs:
        contents = dirs[p]
    else:
        contents = []
    prefix = "  " * len(p)
    dirname = p[-1] if p else "/"
    print(f"{prefix}- {dirname} (dir)")

    for c in contents:
        if c[0] == "dir":
            showdir(dirs, p + (c[1],))
        else:
            size = int(c[0])
            print(f"{prefix}  - {c[1]} (file, size={size})")
            
def showdirs(dirs):
    showdir(dirs, ())
    
def gatherTotalSizes(dirs, sizes, p):
    if p in dirs:
        contents = dirs[p]
    else:
        contents = []

    psize = 0
    for c in contents:
        if c[0] == "dir":
            gatherTotalSizes(dirs, sizes, p + (c[1],))
        else:
            psize += int(c[0])

    if psize > 0:
        for i in range(0,len(p)+1):
            ancestor = p[0:i]
            if not ancestor in sizes:
                sizes[ancestor] = psize
            else:
                sizes[ancestor] = sizes[ancestor] + psize


def totalSize(dirs,p):
    output = 0
    if p in dirs:
        contents = dirs[p]
    else:
        contents = []
    for c in contents:
        if c[0] == "dir":
            output += totalSize(dirs, p + (c[1],))
        else:
            output += int(c[0])
    return output


def processCommands(commands):    
    dirs = { () : [] }
    
    pwd = ()
    for cdata in commands:
        c = cdata[0]
        #print(f"{c} -> {cdata[1:]}")
        
        if c[0] == "ls":
            dirs[pwd] = cdata[1:]
        elif c[0] == "cd":
            if c[1] == "/":
                pwd = ()
            elif c[1] == "..":
                pwd = pwd[:-1]
            else:
                found = False
                for x in dirs[pwd]:
                    if x[0] == "dir" and x[1] == c[1]:
                        found = True
                        break
                newpwd = pwd + (c[1],)
                if not found:
                    print(f"Unknown directory: {newpwd}")
                    dirs[pwd].append( ["dir", c[1]] )
                    dirs[newpwd] = []
                pwd = newpwd

    #showdirs(dirs)
    return dirs

if args.p1:
    print("Doing part 1")

    dirs = processCommands(commands)
    sizes = {}
    gatherTotalSizes(dirs, sizes, () )

    total = 0
    for d,psize in sizes.items():
        if psize <= 100000:
            total += psize
    print(f"Capped Total: {total}")
                
            
if args.p2:
    print("Doing part 2")

    filesystemsize = 70000000
    neededspace = 30000000

    dirs = processCommands(commands)
    sizes = {}
    gatherTotalSizes(dirs, sizes, () )

    used = sizes[()]
    unused = filesystemsize - used

    bestcandidate = ( (), used )
    for d,psize in sizes.items():
        if unused + psize >= neededspace:
            if psize < bestcandidate[1]:
                bestcandidate = (d, psize)

    print(f"Best {bestcandidate}")
